import logging
import os
import re
from typing import Optional, Tuple, Union, List, Any
from urllib.parse import urlencode, urljoin

import dash
import dash_auth
import dash_auth.auth
import requests
from flask import Response, flash, redirect, request, session


class SCDAAuth(dash_auth.auth.Auth):
    """Implements auth via SCDA/QDT OpenID."""

    AUTH_REASON_APP_NOT_ASSOCIATED = "auth_reason_app_not_associated"
    AUTH_REASON_NO_EFFECTIVE_PERMISSIONS = "auth_reason_no_effective_permissions"
    AUTH_REASON_ROUTE_PERMISSION_MISSING = "auth_reason_route_permission_missing"
    AUTH_REASON_SERVICE_ERROR = "auth_reason_service_error"
    AUTH_REASON_USER_NOT_FOUND_IN_AUTH_SERVICE = "auth_reason_user_not_found_in_auth_service"
    AUTH_REASON_APP_ID_MISSING = "auth_reason_app_id_missing"
    AUTH_REASON_INVALID_DECLARED_PERMISSION = "auth_reason_invalid_declared_permission"
    AUTH_REASON_CALLBACK_SECURITY_CONTEXT_MISSING = "auth_reason_callback_security_context_missing"

    def __init__(
        self,
        app: dash.Dash,
        app_name: str,
        secret_key: str,
        auth_url: str,
        login_route: str = "/login",
        logout_route: str = "/logout",
        callback_route: str = "/callback",
        log_signin: bool = False,
        public_routes: Optional[list] = None,
        logout_page: Optional[Union[str, Response]] = None,
        secure_session: bool = False,
    ):
        """
        Secure a Dash app through SCDA/QDT Auth service.

        Parameters
        ----------
        app : dash.Dash
            Dash app to secure
        app_name : str
            Name of the app registered in the SCDA/QDT Auth service
        secret_key : str
            Secret key used to sign the session for the app
        auth_url : str
            URL to the SCDA/QDT Auth service
        login_route : str, optional
            Route to login, by default "/login"
        logout_route : str, optional
            Route to logout, by default "/logout"
        callback_route : str, optional
            Route to callback for the current service. By default "/callback"
        log_signin : bool, optional
            Log sign-ins, by default False
        public_routes : Optional[list], optional
            List of public routes, by default None
        logout_page : Union[str, Response], optional
            Page to redirect to after logout, by default None
        secure_session : bool, optional
            Whether to ensure the session is secure, setting the flasck config
            SESSION_COOKIE_SECURE and SESSION_COOKIE_HTTPONLY to True,
            by default False

        """
        # NOTE: The public routes should be passed in the constructor of the Auth
        # but because these are static values, they are set here as defaults.
        # This is only temporal until a better solution is found. For now it
        # works.
        if public_routes is None:
            public_routes = []

        public_routes.extend(["/scda_login", "/scda_logout", "/callback"])

        super().__init__(app, public_routes = public_routes)

        self.app_name = app_name
        self.auth_url = auth_url
        self.login_route = login_route
        self.logout_route = logout_route
        self.callback_route = callback_route
        self.log_signin = log_signin
        self.logout_page = logout_page
        self.app_id: Optional[str] = None

        if not self.__app_name_registered():
            raise RuntimeError(
                f"App name {app_name} is not registered in the auth service. "
                f"Please register it at {self.auth_url}/register/apps"
            )

        if secret_key is not None:
            if hasattr(app, "server") and app.server is not None:
                app.server.secret_key = secret_key
            else:
                raise RuntimeError(
                    "app.server is None. Ensure that the Dash app is properly initialized before setting the secret_key."
                )

        if app.server.secret_key is None:
            raise RuntimeError(
                """
                app.server.secret_key is missing.
                Generate a secret key in your Python session
                with the following commands:
                >>> import os
                >>> import base64
                >>> base64.b64encode(os.urandom(30)).decode('utf-8')
                and assign it to the property app.server.secret_key
                (where app is your dash app instance), or pass is as
                the secret_key argument to SCDAAuth.__init__.
                Note that you should not do this dynamically:
                you should create a key and then assign the value of
                that key in your code/via a secret.
                """
            )
        if secure_session:
            app.server.config["SESSION_COOKIE_SECURE"] = True
            app.server.config["SESSION_COOKIE_HTTPONLY"] = True

        app.server.add_url_rule(
            login_route,
            endpoint = "scda_login",
            view_func = self.login_request,
            methods = ["GET"],
        )
        app.server.add_url_rule(
            logout_route,
            endpoint = "scda_logout",
            view_func = self.logout,
            methods = ["GET"],
        )
        app.server.add_url_rule(
            callback_route,
            endpoint = "callback",
            view_func = self.callback,
            methods = ["GET"],
        )


    def registration_request(self) -> Response:
        registration_url = urljoin(self.auth_url, "/register/user")
        query_params = urlencode({'app': self.app_name})
        full_url = f"{registration_url}?{query_params}"
        return redirect(full_url)


    def permission_request(self) -> Response:
        permissions_url = urljoin(self.auth_url, "/request-permissions")
        permission_route = session.get("missing_permission_detail", '')
        permission_action = "view" # Default action is always 'view' for now
        query_params = urlencode(
            {
                'app': self.app_name,
                'permission_route': permission_route,
                'permission_action': permission_action
            }
        )
        full_url = f"{permissions_url}?{query_params}"
        return redirect(full_url)


    def login_request(self) -> Response:
        if session.get("needs_registration", False):
            session.pop("needs_registration")
            return self.registration_request()

        if session.get("needs_permissions", False):
            flash("You need to request permissions for this app. Please contact an administrator.")
            return self.permission_request()

        next_url = request.url_root
        auth_url_with_next = urljoin(self.auth_url, '/login')
        query_params = urlencode({'next': next_url})
        full_url = f"{auth_url_with_next}?{query_params}"
        return redirect(full_url)


    def logout(self):
        session.clear()
        base_url = self.app.config.get("url_base_pathname") or "/"
        page = self.logout_page or f"""
        <div style="display: flex; flex-direction: column;
        gap: 0.75rem; padding: 3rem 5rem;">
            <div>Logged out successfully</div>
            <div><a href="{base_url}">Go back</a></div>
        </div>
        """
        return page


    def callback(self):
        token = request.args.get("token")
        next_url = request.args.get("next", self.app.config["routes_pathname_prefix"])

        if not token:
            logging.error("No token received in callback.")
            return redirect(self.login_request())

        response = redirect(next_url)
        response.set_cookie(
            "access_token",
            token,
            httponly = True,
            max_age = 60 * 60 * 24 * 7,
            domain = None,
            path = "/",
        )

        return response


    def is_authorized(self) -> bool:
        if session.get("needs_permissions", False):
            return False

        authorized = False

        access_token_cookie = request.cookies.get("access_token", None)
        access_token_header = request.headers.get("Authorization", None)

        if not access_token_cookie:
            if not access_token_header:
                return authorized
            else:
                access_token = re.sub("Bearer ", "", access_token_header)
        else:
            access_token = access_token_cookie

        try:
            logged_in, token_payload = self.verify_token(access_token)
        except Exception as e:
            logging.exception(f"Error verifying token: {e}")
            return authorized

        if logged_in:
            authorized = self.check_user_authorization(
                token_payload["user_info"]["id"], access_token
            )
            if authorized:
                session["user"] = token_payload.get("user_info")
                session.pop("needs_registration", None)
                session.pop("needs_permissions", None)
                return authorized
            else:
                failure_reason_code = session.get('authorization_failure_reason')
                flash_message = "Access denied. "

                if failure_reason_code == self.AUTH_REASON_APP_NOT_ASSOCIATED:
                    flash_message = f"You are not associated with the application '{self.app_name}'. Please request access."
                    session['needs_registration'] = True

                elif failure_reason_code == self.AUTH_REASON_NO_EFFECTIVE_PERMISSIONS:
                    session['needs_permissions'] = True
                    flash_message = f"You have no permissions within the application '{self.app_name}'. Please contact an administrator."

                elif failure_reason_code == self.AUTH_REASON_ROUTE_PERMISSION_MISSING:
                    session['needs_permissions'] = True
                    flash_message = "You do not have permission to access this page. Please request access."

                elif failure_reason_code == self.AUTH_REASON_USER_NOT_FOUND_IN_AUTH_SERVICE:
                    flash_message = "Your user account was not found. Please register or contact support."
                    session['needs_registration'] = True

                elif failure_reason_code == self.AUTH_REASON_SERVICE_ERROR:
                    flash_message = "Could not verify your authorization due to a service error. Please try again later."

                else:
                    flash_message += "You may not have the necessary permissions."

                flash(flash_message)
                return authorized
        else:
            flash("Your session is invalid or has expired. Please log in again.")
            return authorized


    def verify_token(self, token: str) -> Tuple[bool, dict]:
        try:
            response = requests.post(
                self.auth_url + "/verify_token",
                json = {
                    "access_token": token,
                    "token_type": "bearer",
                }
            )
            response.raise_for_status()
            is_verified = response.json()["is_verified"]
            return is_verified, response.json()["token_payload"]
        except requests.exceptions.RequestException as e:
            logging.exception(f"Error verifying token: {e}")
            return False, {}


    def __app_name_registered(self) -> bool:
        url_app_path = f"/apps/name/{self.app_name}"
        url = urljoin(self.auth_url, url_app_path)
        try:
            response = requests.get(url)
            response.raise_for_status()
            app_data = response.json()
            if self.app_name == app_data.get("name"):
                self.app_id = app_data.get("id")
                if self.app_id is None:
                    logging.error(
                        f"App name {self.app_name} found but 'id' is missing in the response from {url}."
                    )
                    return False
                return True
            else:
                logging.warning(
                    f"App name {self.app_name} does not match the name in the response from {url}."
                )
                return False
        except requests.exceptions.RequestException as e:
            if isinstance(e, requests.exceptions.HTTPError) and e.response.status_code == 404:
                logging.exception(
                    f"App name {self.app_name} not registered in auth service. "
                    f"Did you register it? You can request a registration at {self.auth_url}/register/apps"
                )
            if isinstance(e, requests.exceptions.HTTPError) and e.response.status_code == 500:
                logging.exception(
                    f"Internal server error when verifying app name. "
                    f"Please try again later or contact the administrator."
                )
                raise
            logging.exception(f"Unexpected error when verifying app name: {e}")

            return False

    def get_user_effective_permissions(self, user_id: str, access_token: str) -> Tuple[Optional[List[dict]], Optional[str]]:
        """
        Get all effective permissions for a user within this app.
        """
        if not self.app_id:
            logging.error(
                "Cannot get user effective permissions: app_id is not set."
            )
            return None, self.AUTH_REASON_APP_ID_MISSING

        permissions_url = urljoin(
            self.auth_url, f"/apps/{self.app_id}/users/{user_id}/permissions/effective"
        )

        headers = {"Authorization": f"Bearer {access_token}"}

        try:
            response = requests.get(permissions_url, headers = headers)
            response.raise_for_status()
            permissions_response = response.json()
            logging.debug(
                f"Effective permissions for user {user_id} in app {self.app_name}: {permissions_response.get('count', 0)}"
            )
            return permissions_response.get("data", []), None

        except requests.exceptions.HTTPError as e:
            logging.error(f"HTTP error fetching effective permissions from {permissions_url} for user {user_id}, app {self.app_id}")
            return None, self.AUTH_REASON_SERVICE_ERROR

        except requests.exceptions.RequestException as e:
            logging.error(
                f"Network error fetching effective permissions from {permissions_url} for user {user_id}, app {self.app_id}: {e}",
            )
            return None, self.AUTH_REASON_SERVICE_ERROR

        except ValueError:
            logging.error(
                f"Failed to decode JSON response from {permissions_url} "
                f"when fetching effective permissions for user {user_id}, app {self.app_id}.",
            )
            return None, self.AUTH_REASON_SERVICE_ERROR

    def check_user_authorization(self, user_id: str, access_token: str) -> bool:
        user_apps_url = urljoin(self.auth_url, f"/users/{user_id}/apps")
        try:
            response = requests.get(user_apps_url, headers = {"Authorization": f"Bearer {access_token}"})
            response.raise_for_status()
            user_apps_json = response.json()

            if self.app_name not in [_app.get('name') for _app in user_apps_json.get('data', [])]:
                logging.warning(
                    f"User {user_id} is not authorized for app {self.app_name} (not in user's app list)."
                )
                session['authorization_failure_reason'] = self.AUTH_REASON_APP_NOT_ASSOCIATED
                return False
        except requests.exceptions.HTTPError as e:
            log_msg = f"HTTP error checking app association for user {user_id} at {user_apps_url}"
            reason = self.AUTH_REASON_SERVICE_ERROR
            if e.response is not None:
                log_msg += f", status: {e.response.status_code}, response: {e.response.text}"
                if e.response.status_code == 404:
                    reason = self.AUTH_REASON_USER_NOT_FOUND_IN_AUTH_SERVICE
            else:
                log_msg += "."
            logging.error(log_msg, exc_info = True)
            session['authorization_failure_reason'] = reason
            return False
        except requests.exceptions.RequestException as e:
            logging.error(
                f"Network error checking app association for user {user_id} at {user_apps_url}: {e}",
                exc_info = True
            )
            session['authorization_failure_reason'] = self.AUTH_REASON_SERVICE_ERROR
            return False
        except ValueError:
            logging.error(
                f"Failed to decode JSON from {user_apps_url} checking app association for user {user_id}.",
                exc_info = True
            )
            session['authorization_failure_reason'] = self.AUTH_REASON_SERVICE_ERROR
            return False

        effective_permissions_data, perm_fetch_failure_reason = self.get_user_effective_permissions(user_id, access_token)
        if perm_fetch_failure_reason:
            session['authorization_failure_reason'] = perm_fetch_failure_reason
            return False
        if effective_permissions_data is None:
             logging.error(f"Effective permissions data is None for user {user_id}, app {self.app_name}, but no failure reason was set from get_user_effective_permissions.")
             session['authorization_failure_reason'] = self.AUTH_REASON_SERVICE_ERROR
             return False

        user_permission_names_set = {p.get('name') for p in effective_permissions_data if p.get('name')}
        session['user_permissions'] = list(user_permission_names_set)

        if not user_permission_names_set and effective_permissions_data is not None:
            logging.warning(f"User {user_id} associated with app {self.app_name} but has no effective permissions.")
            session['authorization_failure_reason'] = self.AUTH_REASON_NO_EFFECTIVE_PERMISSIONS
            return False


        current_request_path = request.path
        required_permission_str = None

        if current_request_path == "/_dash-update-component":
            body = request.get_json()
            inputs = body.get("inputs", [])
            declared_resource_permission = None

            for inp in inputs:
                if isinstance(inp, dict) and inp.get("property") == "data":
                    inp_id = inp.get("id")
                    if isinstance(inp_id, dict) and inp_id.get("type") == "scda-permission-context":
                        declared_resource_permission = inp.get("value")
                        break

            if declared_resource_permission:
                if not isinstance(declared_resource_permission, str):
                    logging.error(
                        f"Invalid declared permission type: {type(declared_resource_permission)}. Expected str."
                    )
                    session['authorization_failure_reason'] = self.AUTH_REASON_INVALID_DECLARED_PERMISSION
                    return False
                required_permission_str = declared_resource_permission
            else:
                # Fallback: no permission decalred by callback.
                # Checking if the user can access the pathname of the current request.
                page_pathname_from_inputs = None
                for inp in inputs:
                    if isinstance(inp, dict) and inp.get("property") == "pathname":
                        page_pathname_from_inputs = inp.get("value")
                        break

                if page_pathname_from_inputs:
                    required_permission_str = f"{self.app_name}:{page_pathname_from_inputs}:view"
                    logging.info(
                        f"No declared permission found in inputs. Using pathname {page_pathname_from_inputs} "
                    )
                else:
                    logging.warning(
                        "No declared permission found in inputs and no pathname available. "
                    )
                    session['authorization_failure_reason'] = self.AUTH_REASON_CALLBACK_SECURITY_CONTEXT_MISSING
                    return False
        else:
            required_permission_str = f"{self.app_name}:{current_request_path}:view"

        if not required_permission_str:
            logging.error(f"Internal error: required_permission_str not set for {current_request_path}")
            session['authorization_failure_reason'] = "internal_auth_error"
            return False

        if required_permission_str in user_permission_names_set:
            logging.info(
                f"User {user_id} authorized for route {current_request_path} via permission '{required_permission_str}'."
            )
            if 'authorization_failure_reason' in session:
                session.pop('authorization_failure_reason', None)
                session.pop('missing_permission_detail', None)
            return True
        else:
            logging.warning(
                f"User {user_id} denied access to {current_request_path}. "
                f"Missing required permission: '{required_permission_str}'. "
                f"Available permissions: {user_permission_names_set}"
            )
            session['authorization_failure_reason'] = self.AUTH_REASON_ROUTE_PERMISSION_MISSING
            session['missing_permission_detail'] = required_permission_str
            return False


    def check_current_user_authorization(self) -> bool:
        """
        Check if the current user is authorized to access the app. This method
        expects the user to be logged in and the user info to be stored in the
        session.
        """
        url = urljoin(self.auth_url, "/users/me/apps")
        try:
            access_token = request.cookies.get("access_token", None)
            response = requests.get(url, headers = {"Authorization": f"Bearer {access_token}"})
            response.raise_for_status()
            return response.json().get("is_authorized", False)
        except requests.exceptions.RequestException as e:
            logging.exception(f"Error checking user authorization: {e}")
            return False
