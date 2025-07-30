import os
import json
import requests
from datetime import datetime, timezone
from erioon.database import Database

class ErioonClient:
    """
    Client SDK for interacting with the Erioon API.

    Handles:
    - User authentication with email/password and API key
    - Token caching to avoid re-authenticating every time
    - SAS token expiration detection and auto-renewal
    - Access to user-specific databases
    """

    def __init__(self, api, email, password, base_url="https://sdk.erioon.com"):
        self.api = api
        self.email = email
        self.password = password
        self.base_url = base_url
        self.user_id = None
        self.error = None
        self.token_path = os.path.expanduser(f"~/.erioon_token_{self._safe_filename(email)}")
        self.login_metadata = None

        try:
            self.login_metadata = self._load_or_login()
            self._update_metadata_fields()
        except Exception as e:
            self.error = str(e)

    def _safe_filename(self, text):
        """
        Converts unsafe filename characters to underscores for cache file naming.
        """
        return "".join(c if c.isalnum() else "_" for c in text)

    def _do_login_and_cache(self):
        """
        Logs in to the API and writes the returned metadata (e.g. SAS token, user ID) to a local file.
        """
        metadata = self._login()
        with open(self.token_path, "w") as f:
            json.dump(metadata, f)
        return metadata

    def _load_or_login(self):
        """
        Tries to load the cached login metadata.
        If token is expired or file does not exist, performs a fresh login.
        """
        if os.path.exists(self.token_path):
            with open(self.token_path, "r") as f:
                metadata = json.load(f)
            if self._is_sas_expired(metadata):
                metadata = self._do_login_and_cache()
            return metadata
        else:
            return self._do_login_and_cache()

    def _login(self):
        """
        Sends login request to Erioon API using API key, email, and password.
        Returns authentication metadata including SAS token.
        """
        url = f"{self.base_url}/login_with_credentials"
        payload = {"api_key": self.api, "email": self.email, "password": self.password}
        headers = {"Content-Type": "application/json"}

        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            self.login_metadata = data
            self._update_metadata_fields()
            return data
        else:
            raise Exception("Invalid account")

    def _update_metadata_fields(self):
        """
        Updates internal fields like user_id, database name, and cluster info
        from login metadata.
        """
        if self.login_metadata:
            self.user_id = self.login_metadata.get("_id")
            self.database = self.login_metadata.get("database")
            self.cluster = self.login_metadata.get("cluster")

    def _clear_cached_token(self):
        """
        Clears the locally cached authentication token and resets internal state.
        """
        if os.path.exists(self.token_path):
            os.remove(self.token_path)
        self.user_id = None
        self.login_metadata = None

    def _is_sas_expired(self, metadata):
        """
        Determines whether the SAS token has expired by comparing the 'sas_token_expiry'
        or 'expiry' field with the current UTC time.
        """
        expiry_str = metadata.get("sas_token_expiry") or metadata.get("expiry")

        if not expiry_str:
            return True

        try:
            expiry_dt = datetime.fromisoformat(expiry_str.replace("Z", "+00:00"))
            now = datetime.now(timezone.utc)
            return now >= expiry_dt
        except Exception:
            return True

    def __getitem__(self, db_id):
        """
        Allows syntax like `client["my_database_id"]` to access a database.
        If the token is expired or invalid, it attempts reauthentication.
        """
        if not self.user_id:
            raise ValueError("Client not authenticated. Cannot access database.")

        try:
            return self._get_database_info(db_id)
        except Exception as e:
            err_msg = str(e).lower()
            if f"database with {db_id.lower()}" in err_msg or "database" in err_msg:
                self._clear_cached_token()
                try:
                    self.login_metadata = self._do_login_and_cache()
                    self._update_metadata_fields()
                except Exception:
                    return "Login error"

                try:
                    return self._get_database_info(db_id)
                except Exception:
                    return f"❌ Database with _id {db_id} ..."
            else:
                raise e

    def _get_database_info(self, db_id):
        """
        Sends a POST request to fetch metadata for a given database ID.
        Returns a `Database` instance initialized with SAS URL and metadata.
        """
        payload = {"user_id": self.user_id, "db_id": db_id}
        headers = {"Content-Type": "application/json"}

        response = requests.post(f"{self.base_url}/db_info", json=payload, headers=headers)

        if response.status_code == 200:
            db_info = response.json()

            container_url = self.login_metadata.get("container_url")
            sas_token = self.login_metadata.get("sas_token")

            if not container_url or not sas_token:
                raise Exception("Missing SAS URL components for storage access")

            if not sas_token.startswith("?"):
                sas_token = "?" + sas_token

            sas_url = container_url.split("?")[0] + sas_token

            return Database(
                user_id=self.user_id,
                metadata=db_info,
                database=self.database,
                cluster=self.cluster,
                sas_url=sas_url
            )
        else:
            try:
                error_json = response.json()
                error_msg = error_json.get("error", response.text)
            except Exception:
                error_msg = response.text
            raise Exception(error_msg)

    def __str__(self):
        """
        Returns user_id or error string when printed.
        """
        return self.user_id if self.user_id else self.error

    def __repr__(self):
        """
        Developer-friendly representation of the client.
        """
        return f"<ErioonClient user_id={self.user_id}>" if self.user_id else f"<ErioonClient error='{self.error}'>"
