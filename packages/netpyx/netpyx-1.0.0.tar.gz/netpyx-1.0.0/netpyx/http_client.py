import requests
import logging
from typing import Dict, Any, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HttpClient:
    """
    A reusable HTTP client for making structured API requests using the `requests` library.

    Features:
    - Supports GET, POST, PUT, DELETE HTTP methods.
    - Header, cookie, and authentication management (Basic and Bearer).
    - Optional base URL to simplify endpoint handling.
    - Cookie tracking from server responses.
    - Context manager support with `with` syntax.
    """

    def __init__(self, base_url: str = "") -> None:
        """
        Initialize the HTTP client.

        Args:
            base_url (str): Base URL used to prefix all relative endpoints.
        """
        self.session = requests.Session()
        self.base_url = base_url

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_session()

    def _full_url(self, endpoint: str) -> str:
        """
        Construct the complete URL from the base URL and endpoint.

        Args:
            endpoint (str): A relative path or an absolute URL.

        Returns:
            str: The full URL to send the request to.
        """
        if endpoint.startswith(('http://', 'https://')):
            return endpoint
        return f"{self.base_url}{endpoint}"

    def set_headers(self, headers: Dict[str, str]) -> None:
        """
        Set or update global headers for all future requests.

        Args:
            headers (Dict[str, str]): A dictionary of header key-value pairs.
        """
        self.session.headers.update(headers)
        logger.info(f"Headers updated: {self.session.headers}")

    def set_user_agent(self, user_agent: str) -> None:
        """
        Set a custom User-Agent header.

        Args:
            user_agent (str): The user agent string to use.
        """
        self.session.headers.update({"User-Agent": user_agent})
        logger.info(f"User-Agent set to: {user_agent}")

    def set_cookies(self, cookies: Dict[str, str]) -> None:
        """
        Manually set or update cookies.

        Args:
            cookies (Dict[str, str]): A dictionary of cookie key-value pairs.
        """
        self.session.cookies.update(cookies)
        logger.info(f"Cookies updated: {self.session.cookies.get_dict()}")

    def set_auth(self, auth: tuple[str, str]) -> None:
        """
        Set Basic Authentication credentials.

        Args:
            auth (tuple[str, str]): A tuple containing (username, password).
        """
        self.session.auth = auth
        logger.info(f"Basic authentication configured for user: {auth[0]}")

    def set_auth_bearer(self, token: str) -> None:
        """
        Set Bearer token authentication.

        Args:
            token (str): The Bearer token string.
        """
        self.session.headers.update({"Authorization": f"Bearer {token}"})
        logger.info("Bearer authentication configured.")

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, **kwargs) -> Optional[requests.Response]:
        """
        Perform a GET request.

        Args:
            endpoint (str): Relative endpoint or absolute URL.
            params (Optional[Dict[str, Any]]): URL query parameters.
            **kwargs: Additional arguments for requests.get().

        Returns:
            Optional[requests.Response]: The response object, or None on failure.
        """
        full_url = self._full_url(endpoint)
        logger.info(f"GET: {full_url}, Params: {params}")
        try:
            response = self.session.get(full_url, params=params, **kwargs)
            response.raise_for_status()
            self.session.cookies.update(response.cookies)
            return response
        except requests.RequestException as e:
            logger.error(f"GET request failed: {e}")
            return None

    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None,
             json: Optional[Dict[str, Any]] = None, **kwargs) -> Optional[requests.Response]:
        """
        Perform a POST request.

        Args:
            endpoint (str): Relative endpoint or absolute URL.
            data (Optional[Dict[str, Any]]): Form data.
            json (Optional[Dict[str, Any]]): JSON payload.
            **kwargs: Additional arguments for requests.post().

        Returns:
            Optional[requests.Response]: The response object, or None on failure.
        """
        full_url = self._full_url(endpoint)
        logger.info(f"POST: {full_url}, Data: {data}, JSON: {json}")
        try:
            response = self.session.post(full_url, data=data, json=json, **kwargs)
            response.raise_for_status()
            self.session.cookies.update(response.cookies)
            return response
        except requests.RequestException as e:
            logger.error(f"POST request failed: {e}")
            return None

    def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None,
            json: Optional[Dict[str, Any]] = None, **kwargs) -> Optional[requests.Response]:
        """
        Perform a PUT request.

        Args:
            endpoint (str): Relative endpoint or absolute URL.
            data (Optional[Dict[str, Any]]): Form data.
            json (Optional[Dict[str, Any]]): JSON payload.
            **kwargs: Additional arguments for requests.put().

        Returns:
            Optional[requests.Response]: The response object, or None on failure.
        """
        full_url = self._full_url(endpoint)
        logger.info(f"PUT: {full_url}, Data: {data}, JSON: {json}")
        try:
            response = self.session.put(full_url, data=data, json=json, **kwargs)
            response.raise_for_status()
            self.session.cookies.update(response.cookies)
            return response
        except requests.RequestException as e:
            logger.error(f"PUT request failed: {e}")
            return None

    def delete(self, endpoint: str, **kwargs) -> Optional[requests.Response]:
        """
        Perform a DELETE request.

        Args:
            endpoint (str): Relative endpoint or absolute URL.
            **kwargs: Additional arguments for requests.delete().

        Returns:
            Optional[requests.Response]: The response object, or None on failure.
        """
        full_url = self._full_url(endpoint)
        logger.info(f"DELETE: {full_url}")
        try:
            response = self.session.delete(full_url, **kwargs)
            response.raise_for_status()
            self.session.cookies.update(response.cookies)
            return response
        except requests.RequestException as e:
            logger.error(f"DELETE request failed: {e}")
            return None

    def get_cookies(self) -> Dict[str, str]:
        """
        Retrieve the current cookies stored in the session.

        Returns:
            Dict[str, str]: A dictionary of cookies.
        """
        return self.session.cookies.get_dict()

    def close_session(self) -> None:
        """
        Close the HTTP session and release system resources.
        """
        self.session.close()
        logger.info("HTTP session closed.")
