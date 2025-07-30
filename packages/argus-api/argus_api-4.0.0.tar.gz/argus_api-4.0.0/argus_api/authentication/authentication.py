from typing import TYPE_CHECKING, Optional, List, Union


try:
    from typing import runtime_checkable, Protocol
except ImportError:
    from typing_extensions import runtime_checkable, Protocol


import requests
from argus_api._validators import validate_http_response
from argus_api.utils import _load_cli_settings
from argus_api.exceptions.http import ArgusException
from argus_api.exceptions.client import ArgusAPIAuthenticationError
from argus_api.authentication.csrf import get_CSRF_token

if TYPE_CHECKING:
    from argus_api.session import ArgusAPISession


@runtime_checkable
class SupportsRefresh(Protocol):
    def refresh(self, session: "ArgusAPISession") -> None:
        ...

    def should_refresh(self) -> bool:
        ...


class ArgusAPIAuth:
    """Base authentication class.

    Defines the interface for authentication classes, but should not be used directly
    as does not perform any authentication.
    """

    is_authenticated: bool = False
    #: indicates that this authentication method needs a manual check to confirm
    #: success - for auth methods that do not touch the backend on authentication
    #: (API key, pre-existing session token...)
    _needs_check_query: bool = False
    #: indicates that this authentication method requires a CSRF token
    _needs_CSRF_token: bool = False

    def __call__(self, url):
        return self.headers

    @property
    def headers(self) -> Optional[dict]:
        return None

    @property
    def cookies(self) -> Optional[dict]:
        return None

    def authenticate(self, api_url: str):
        """authenticate the auth object.

        this should perform any required operations (for ex. sending an authentication
        request and retrieving a token) and save all reauired state on the auth object.
        """
        self.is_authenticated = True

    def authenticate_session(self, session: "ArgusAPISession"):
        """authenticate the given session.

        Unlike the authenticate method, this should set the session objects's internal
        session (its :class:`requests.Session` instance) state.
        """
        if not self.is_authenticated:
            self.authenticate(session.base_url)
        if self.headers:
            session._session.headers.update(self.headers)
        if self.cookies:
            session._session.cookies.update(self.cookies)
        session.authenticated = True

    def cleanup_session(self, session: "ArgusAPISession"):
        """Remove authentication state set by the auth object on the given session.

        this is used when changing the authentication object used by a session.
        """
        if self.headers:
            session._session.headers.update({k: None for k in self.headers.keys()})
        session._session.cookies.clear_session_cookies()
        session.authenticated = False

    def __eq__(self, other):
        """Compare two auth objects.

        Comparison is necessary to determine whether authentication settings have
        changed when the argus_cli settings are used.
        """
        return (type(other) is type(self)) and (other is self)


class APIKeyAuth(ArgusAPIAuth):
    """API key authentication interface."""

    _needs_check_query = True

    def __init__(self, api_key: str):
        """
        :param api_key: Argus API key.
        """
        self.api_key = api_key
        self.is_authenticated = True

    @property
    def headers(self) -> dict:
        return {"Argus-API-Key": self.api_key}

    def authenticate_session(self, session: "ArgusAPISession"):
        session._session.headers.update(self.headers)
        session.authenticated = True

    def __eq__(self, other):
        if type(other) == type(self):
            return other.api_key == self.api_key
        return False


class PasswordBasedSessionAuthentication(ArgusAPIAuth):
    """Common password-based session authentication interface.

    This class is an internal utility used to factor functionality common to LDAP and
    password authentication classes.
    """

    _needs_CSRF_token = True
    DEFAULT_DOMAIN = "MNEMONIC"

    @property
    def cookies(self) -> Optional[dict]:
        return self._cookies

    @property
    def authentication_route(self):
        return f"/authentication/v1/{self.method}/authentication"

    def __init__(
        self,
        method: str,
        username: str,
        password: str,
        domain: Optional[str] = None,
        request_authorizations: Optional[List[str]] = None,
    ):
        """Initialize a PasswordBasedSessionAuthentication object.

        :param method: authentication method - currently either "password" or "ldap"
        :param username: user to authenticate
        :param password: password to authenticate with
        :param request_authorizations: additional special authorizations to request
        """
        if method not in ("password", "ldap"):
            raise ValueError(f"unsupported method: {method}")
        self.method = method
        self.username = username
        self.password = password
        self.domain = domain or self.DEFAULT_DOMAIN
        self.request_authorizations = request_authorizations
        self.session_key = None
        self.session_token = None
        self._cookies = None
        self.is_authenticated = False

    def _post_auth(
        self, session_or_base_url: Union["ArgusAPISession", str], mutate_session=True
    ):
        """perform the authentication request.

         :param session_or_base_url: either a session object or the API base URL.
            if ``mutate_session`` is set to ``True``, must be a session object.
        :param mutate_session: if set to ``True``, will set authentication state
           (cookies) on the session.
        """
        if isinstance(session_or_base_url, str):
            base_url = session_or_base_url
            if mutate_session:
                raise ValueError("can not mutate session, a base URL was passed.")
        else:
            base_url = session_or_base_url.base_url
        url = f"{base_url}{self.authentication_route}"
        payload = {
            "userName": self.username,
            "password": self.password,
            "domain": self.domain,
        }
        if self.request_authorizations:
            payload["requestedAuthorizations"] = self.request_authorizations
        if mutate_session:
            response = session_or_base_url._session.post(url, json=payload)
        else:
            response = requests.post(url, json=payload)
        try:
            validate_http_response(response)
        except ArgusException as e:
            raise ArgusAPIAuthenticationError(response=response) from e
        return response

    def authenticate(self, api_url: str):
        response = self._post_auth(api_url, mutate_session=False)
        self._cookies = dict(response.cookies)
        try:
            rdata = response.json()
            self.session_key = rdata["data"]["sessionKey"]
            self.session_token = rdata["data"]["credentials"]["requestCredentialsData"]
        except Exception as e:
            raise ArgusAPIAuthenticationError(
                message=f"error reading server response: {e}", response=response
            )
        self.is_authenticated = True

    def authenticate_session(self, session: "ArgusAPISession"):
        response = self._post_auth(session, mutate_session=True)

        try:
            rdata = response.json()
            self.session_key = rdata["data"]["sessionKey"]
            self.session_token = rdata["data"]["credentials"]["requestCredentialsData"]
        except Exception as e:
            raise ArgusAPIAuthenticationError(
                message=f"error reading server response: {e}", response=response
            )
        self.is_authenticated = True
        session.authenticated = True

    def get_CSRF_token(self, url: str) -> str:
        """get a CSRF token for the given URL."""

        return get_CSRF_token(url, self.session_key)

    def __eq__(self, other):
        if type(other) == type(self):
            return all(
                [
                    (other.method == self.method),
                    (other.username == self.username),
                    (other.password == self.password),
                    (other.domain == self.domain),
                ]
            )
        return False


class PasswordAuthentication(PasswordBasedSessionAuthentication):
    """Password authentication."""

    def __init__(
        self,
        username: str,
        password: str,
        domain: Optional[str] = None,
        request_authorizations: Optional[List[str]] = None,
    ):
        """
        :param username: user to authenticate
        :param password: password to authenticate with
        :param domain: domain to authenticate within
        :param request_authorizations: additional special authorizations to request
        """
        super().__init__(
            method="password",
            username=username,
            password=password,
            domain=domain,
            request_authorizations=request_authorizations,
        )


class LDAPAuthentication(PasswordBasedSessionAuthentication):
    def __init__(
        self,
        username: str,
        password: str,
        domain: Optional[str] = None,
        request_authorizations: Optional[List[str]] = None,
    ):
        """
        :param username: user to authenticate
        :param password: password to authenticate with
        :param domain: domain to authenticate within
        :param request_authorizations: additional special authorizations to request
        """
        super().__init__(
            method="ldap",
            username=username,
            password=password,
            domain=domain,
            request_authorizations=request_authorizations,
        )


def get_auth_from_cli_config() -> ArgusAPIAuth:
    """construct an authentication object from argus_cli settings."""
    settings = _load_cli_settings()
    api_settings = settings.get("api", {})
    method = api_settings.get("method", "apikey")
    if method == "apikey":
        api_key = api_settings.get("api_key")
        return APIKeyAuth(api_key=api_key)
    elif method in ("password", "ldap"):
        username = api_settings.get("username")
        password = api_settings.get("password")
        domain = api_settings.get("domain")
        if method == "password":
            cls = PasswordAuthentication
        elif method == "ldap":
            cls = LDAPAuthentication
        return cls(username=username, password=password, domain=domain)


class SessionTokenAuth(ArgusAPIAuth):
    """Session token authorization."""

    _needs_check_query = True

    @property
    def headers(self) -> dict:
        return {"Authorization": f"Bearer {self.session_token}"}

    def __init__(
        self,
        session_token: str,
    ):
        """Initialize a SessionTokenAuth object.

        :param session_token: Argus session token (argus_session cookie).
        """
        self.session_token = session_token
        self._cookies = {"argus_session": self.session_token}
        self.is_authenticated = True

    def authenticate_session(self, session: "ArgusAPISession"):
        session._session.headers.update(self.headers)
        session.authenticated = True

    def __eq__(self, other):
        if type(other) == type(self):
            return self.session_token == other.session_token
        return False
