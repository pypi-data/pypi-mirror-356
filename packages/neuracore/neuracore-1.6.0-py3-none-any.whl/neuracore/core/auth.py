"""Authentication management for Neuracore API access.

This module provides authentication functionality including API key management,
access token handling, configuration persistence, and version validation.
It implements a singleton pattern to maintain authentication state across
the application.
"""

import json
import os
from pathlib import Path
from typing import Optional

import requests

from .const import API_URL
from .exceptions import AuthenticationError
from .generate_api_key import generate_api_key

CONFIG_DIR = Path.home() / ".neuracore"
CONFIG_FILE = "config.json"


class Auth:
    """Singleton class for managing Neuracore authentication state.

    This class handles API key management, access token retrieval, configuration
    persistence, and provides authenticated request headers. It maintains
    authentication state throughout the application lifecycle and automatically
    loads saved configuration on initialization.
    """

    _instance = None
    _api_key: Optional[str] = None

    def __new__(cls) -> "Auth":
        """Create or return the singleton Auth instance.

        Returns:
            The singleton Auth instance.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """Initialize the Auth instance and load saved configuration."""
        self._load_config()
        self._access_token = None

    def _load_config(self) -> None:
        """Load authentication configuration from persistent storage.

        Attempts to load previously saved API key from the user's home
        directory configuration file. Does nothing if no configuration
        file exists.
        """
        config_file = CONFIG_DIR / CONFIG_FILE
        if config_file.exists():
            with open(config_file) as f:
                config = json.load(f)
                self._api_key = config.get("api_key")

    def _save_config(self) -> None:
        """Save current authentication configuration to persistent storage.

        Creates the configuration directory if it doesn't exist and saves
        the current API key to a JSON configuration file in the user's
        home directory.
        """
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        config_file = CONFIG_DIR / CONFIG_FILE
        with open(config_file, "w") as f:
            json.dump({"api_key": self._api_key}, f)

    def login(self, api_key: Optional[str] = None) -> None:
        """Authenticate with the Neuracore server using an API key.

        Attempts authentication using the provided API key, environment variable,
        or saved configuration. If no API key is available, initiates the API
        key generation process. Upon successful verification, saves the
        configuration for future use.

        Args:
            api_key: API key for authentication. If not provided, will attempt
                to use the NEURACORE_API_KEY environment variable or previously
                saved configuration. If none are available, will prompt for
                interactive API key generation.

        Raises:
            AuthenticationError: If API key verification fails due to invalid
                credentials, network issues, or server errors.
        """
        self._api_key = api_key or os.environ.get("NEURACORE_API_KEY") or self._api_key

        if not self._api_key:
            print("No API key provided. Attempting to log you in...")
            self._api_key = generate_api_key()

        # Verify API key with server and get access token
        try:
            response = requests.post(
                f"{API_URL}/auth/verify-api-key",
                json={"api_key": self._api_key},
            )
            if response.status_code != 200:
                raise AuthenticationError(
                    "Could not verify API key. Please check your key and try again."
                )
            token_data = response.json()
            self._access_token = token_data["access_token"]
        except requests.exceptions.RequestException:
            raise AuthenticationError(
                "Could not verify API key. Please check your key and try again."
            )

        # Save configuration if verification successful
        self._save_config()

    def logout(self) -> None:
        """Clear authentication state and remove saved configuration.

        Resets all authentication data including API key and access token,
        and removes the saved configuration file from disk.
        """
        self._api_key = None
        self._access_token = None
        config_file = CONFIG_DIR / CONFIG_FILE
        if config_file.exists():
            config_file.unlink()

    def validate_version(self) -> None:
        """Validate client version compatibility with the Neuracore server.

        Checks that the current Neuracore client version is compatible with
        the server API version. This helps ensure that API calls will work
        correctly and prevents issues from version mismatches.

        Raises:
            AuthenticationError: If version validation fails due to
                incompatible versions or server communication issues.
        """
        # Placeholder for version validation logic
        import neuracore as nc

        response = requests.get(
            f"{API_URL}/auth/verify-version",
            params={"version": nc.__version__},
        )
        if response.status_code != 200:
            raise AuthenticationError(
                f"Version validation failed: {response.json().get('detail')}"
            )

    @property
    def api_key(self) -> Optional[str]:
        """Get the current API key.

        Returns:
            The currently configured API key, or None if not set.
        """
        return self._api_key

    @property
    def access_token(self) -> Optional[str]:
        """Get the current access token.

        Returns:
            The current access token received from the server, or None
            if not authenticated.
        """
        return self._access_token

    @property
    def is_authenticated(self) -> bool:
        """Check if currently authenticated with valid credentials.

        Returns:
            True if both API key and access token are available, indicating
            successful authentication.
        """
        return self._api_key is not None and self._access_token is not None

    def get_headers(self) -> dict:
        """Get HTTP headers for authenticated API requests.

        Provides the authorization header required for making authenticated
        requests to the Neuracore API.

        Returns:
            Dictionary containing the Authorization header with the bearer token.

        Raises:
            AuthenticationError: If not currently authenticated.
        """
        if not self.is_authenticated:
            raise AuthenticationError("Not authenticated. Please call login() first.")
        return {
            "Authorization": f"Bearer {self._access_token}",
        }


# Global instance
_auth = Auth()


def login(api_key: Optional[str] = None) -> None:
    """Global convenience function for authentication.

    Args:
        api_key: Optional API key for authentication.
    """
    _auth.login(api_key)


def logout() -> None:
    """Global convenience function for clearing authentication state."""
    _auth.logout()


def get_auth() -> Auth:
    """Get the global Auth singleton instance.

    Returns:
        The global Auth instance used throughout the application.
    """
    return _auth
