import requests
from typing import Dict, Any, Optional


class HttpClient:
    """
    A reusable HTTP client built on top of the `requests` library.

    Features:
    - Supports GET, POST, PUT, DELETE HTTP methods.
    - Header, cookie, and authentication management (Basic and Bearer).
    - Optional base URL to simplify endpoint usage.
    - Automatic cookie tracking and updating.
    - Context manager support with `with` statement.
    - Optional silent mode to suppress exceptions.
    """

    def __init__(self, base_url: str = "", timeout: int = 10, silent: bool = True) -> None:
        """
        Initialize the HTTP client.

        Args:
            base_url (str, optional): A base URL to prepend to relative endpoints. Defaults to "".
            timeout (int, optional): Default timeout in seconds for each request. Defaults to 10.
            silent (bool, optional): If True, suppresses exceptions on request errors. Defaults to True.
        """
        self.session = requests.Session()
        self.base_url = base_url.rstrip("/") + "/" if base_url else ""
        self.timeout = timeout
        self.silent = silent

    def __enter__(self):
        """Enable usage as a context manager."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Automatically close the session when used in a `with` block."""
        self.close_session()

    def _full_url(self, endpoint: str) -> str:
        """
        Build the full URL based on base_url and the given endpoint.

        Args:
            endpoint (str): Either a relative path or a full URL.

        Returns:
            str: The complete request URL.
        """
        return endpoint if endpoint.startswith(('http://', 'https://')) else f"{self.base_url}{endpoint.lstrip('/')}"

    def _request(self, method: str, endpoint: str, **kwargs) -> Optional[requests.Response]:
        """
        Internal method to make an HTTP request.

        Args:
            method (str): HTTP method (e.g., "GET", "POST", etc.).
            endpoint (str): Endpoint to be called.
            **kwargs: Additional arguments passed to `requests.request`.

        Returns:
            Optional[requests.Response]: Response object or None if request failed and silent is True.
        """
        full_url = self._full_url(endpoint)
        kwargs.setdefault("timeout", self.timeout)

        try:
            response = self.session.request(method, full_url, **kwargs)
            response.raise_for_status()
            self.session.cookies.update(response.cookies)
            return response
        except requests.RequestException:
            if not self.silent:
                raise
            return None

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, **kwargs) -> Optional[requests.Response]:
        """
        Send a GET request.

        Args:
            endpoint (str): Endpoint or full URL.
            params (dict, optional): URL query parameters.
            **kwargs: Additional arguments for `requests.get`.

        Returns:
            Optional[requests.Response]: Response object or None on failure.
        """
        return self._request("GET", endpoint, params=params, **kwargs)

    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None,
             json: Optional[Dict[str, Any]] = None, **kwargs) -> Optional[requests.Response]:
        """
        Send a POST request.

        Args:
            endpoint (str): Endpoint or full URL.
            data (dict, optional): Form data to send.
            json (dict, optional): JSON data to send.
            **kwargs: Additional arguments for `requests.post`.

        Returns:
            Optional[requests.Response]: Response object or None on failure.
        """
        return self._request("POST", endpoint, data=data, json=json, **kwargs)

    def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None,
            json: Optional[Dict[str, Any]] = None, **kwargs) -> Optional[requests.Response]:
        """
        Send a PUT request.

        Args:
            endpoint (str): Endpoint or full URL.
            data (dict, optional): Form data to send.
            json (dict, optional): JSON data to send.
            **kwargs: Additional arguments for `requests.put`.

        Returns:
            Optional[requests.Response]: Response object or None on failure.
        """
        return self._request("PUT", endpoint, data=data, json=json, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> Optional[requests.Response]:
        """
        Send a DELETE request.

        Args:
            endpoint (str): Endpoint or full URL.
            **kwargs: Additional arguments for `requests.delete`.

        Returns:
            Optional[requests.Response]: Response object or None on failure.
        """
        return self._request("DELETE", endpoint, **kwargs)

    def set_headers(self, headers: Dict[str, str]) -> None:
        """
        Set or update global headers for all future requests.

        Args:
            headers (dict): Dictionary of headers to set.
        """
        self.session.headers.update(headers)

    def set_user_agent(self, user_agent: str) -> None:
        """
        Set a custom User-Agent header.

        Args:
            user_agent (str): User-Agent string.
        """
        self.session.headers.update({"User-Agent": user_agent})

    def set_cookies(self, cookies: Dict[str, str]) -> None:
        """
        Set or update session cookies.

        Args:
            cookies (dict): Dictionary of cookies to set.
        """
        self.session.cookies.update(cookies)

    def set_auth(self, auth: tuple[str, str]) -> None:
        """
        Set basic HTTP authentication.

        Args:
            auth (tuple): Tuple of (username, password).
        """
        self.session.auth = auth

    def set_auth_bearer(self, token: str) -> None:
        """
        Set Bearer token for Authorization header.

        Args:
            token (str): Bearer token string.
        """
        self.session.headers.update({"Authorization": f"Bearer {token}"})

    def get_cookies(self) -> Dict[str, str]:
        """
        Get the current cookies stored in the session.

        Returns:
            dict: A dictionary of cookie key-value pairs.
        """
        return self.session.cookies.get_dict()

    def close_session(self) -> None:
        """
        Close the HTTP session and release resources.
        """
        self.session.close()
