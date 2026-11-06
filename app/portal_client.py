"""
Talks to the legacy Urja portal. Everything portal-specific lives HERE,
so the rest of the app never knows the portal exists.

TODO: fill the endpoints/fields after inspecting the portal in DevTools
(Network tab -> log in -> click around -> see what requests fire).
"""
import httpx

from app.config import settings


class PortalError(Exception):
    pass


class PortalClient:
    def __init__(self):
        self.http = httpx.Client(
            base_url=settings.portal_url,
            timeout=settings.request_timeout,
            follow_redirects=False,
        )
        self.logged_in = False

    def login(self):
        # TODO: replace path + payload with what the portal's login form actually sends
        resp = self.http.post(
            "/login",
            data={"email": settings.portal_username, "password": settings.portal_password},
        )
        if resp.status_code not in (200, 302):
            raise PortalError(f"Login failed: {resp.status_code}")
        # httpx keeps cookies on self.http automatically (session cookie / token)
        self.logged_in = True

    def _get(self, path: str, **params):
        if not self.logged_in:
            self.login()
        resp = self.http.get(path, params=params)

        # Session expired? (portal may return 401, or redirect to /login) -> re-login once
        if resp.status_code == 401 or (resp.status_code == 302 and "login" in resp.headers.get("location", "")):
            self.login()
            resp = self.http.get(path, params=params)

        if resp.status_code >= 400:
            raise PortalError(f"Portal returned {resp.status_code} for {path}")
        return resp

    # ---- data methods: return plain dicts, routes shape them into models ----

    def list_meters(self, page: int = 1) -> list[dict]:
        resp = self._get("/meters", page=page)  # TODO: real path
        return resp.json()  # TODO: might be HTML -> parse with BeautifulSoup instead

    def get_meter(self, meter_id: str) -> dict:
        resp = self._get(f"/meters/{meter_id}")  # TODO: real path
        return resp.json()

    def get_consumption(self, meter_id: str) -> list[dict]:
        resp = self._get(f"/meters/{meter_id}/consumption")  # TODO: real path
        return resp.json()


portal = PortalClient()
