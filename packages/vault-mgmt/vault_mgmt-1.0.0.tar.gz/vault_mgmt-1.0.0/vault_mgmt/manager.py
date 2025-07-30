import urllib.parse
import webbrowser

import hvac

OIDC_CALLBACK_PORT = 8250
OIDC_REDIRECT_URI = f"http://localhost:{OIDC_CALLBACK_PORT}/oidc/callback"
SELF_CLOSING_PAGE = """
<!doctype html>
<html>
<head>
<script>
window.onload = function load() {
window.open('', '_self', '');
window.close();
};
</script>
</head>
<body>
<p>Authentication successful, you can close the browser now.</p>
<script>
setTimeout(function() {
window.close()
}, 5000);
</script>
</body>
</html>
"""


class VaultManager:
    def __init__(self, vault_addr):
        self.vault_addr = vault_addr
        self.client = None
        self.kv_version_cache = {}  # Cache for KV engine versions

    def authenticate_with_oidc(self, oidc_role=None):
        self.client = hvac.Client(url=self.vault_addr)

        try:
            start_resp = self.client.auth.oidc.oidc_authorization_url_request(
                role=oidc_role, redirect_uri=OIDC_REDIRECT_URI
            )
            auth_url = start_resp["data"]["auth_url"]
            if auth_url == "":
                return None

            params = urllib.parse.parse_qs(auth_url.split("?")[1])
            auth_url_nonce = params["nonce"][0]
            auth_url_state = params["state"][0]

            webbrowser.open(auth_url)
            token = self._login_oidc_get_token()

            auth_result = self.client.auth.oidc.oidc_callback(
                code=token,
                path="oidc",
                nonce=auth_url_nonce,
                state=auth_url_state,
            )
            new_token = auth_result["auth"]["client_token"]
            self.client.token = new_token
            return self.client
        except Exception as e:
            print(f"OIDC authentication failed for {self.vault_addr}: {e}")
            raise

    def _login_oidc_get_token(self):
        from http.server import BaseHTTPRequestHandler, HTTPServer

        class HttpServ(HTTPServer):
            def __init__(self, *args, **kwargs):
                HTTPServer.__init__(self, *args, **kwargs)
                self.token = None

        class AuthHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                params = urllib.parse.parse_qs(self.path.split("?")[1])
                self.server.token = params["code"][0]  # type: ignore
                self.send_response(200)
                self.end_headers()
                self.wfile.write(str.encode(SELF_CLOSING_PAGE))

            def log_message(self, format, *args):
                pass  # Disable logging to the console

        server_address = ("", OIDC_CALLBACK_PORT)
        httpd = HttpServ(server_address, AuthHandler)
        httpd.handle_request()
        return httpd.token

    def is_authenticated(self):
        """Checks if the client is initialized and has a valid token."""
        if self.client:
            return self.client.is_authenticated()
        return False

    def get_vault_version(self):
        """
        Retrieves the version of the Vault server.
        Returns the version string or None if an error occurs.
        """
        if not self.is_authenticated():
            print("Cannot get Vault version: Client not authenticated.")
            return None

        try:
            # The read_health_status method provides server information including the version
            response = self.client.sys.read_seal_status()  # type: ignore
            return response.get("version")
        except hvac.exceptions.VaultError as e:  # type: ignore
            print(f"Failed to retrieve Vault version from {self.vault_addr}: {e}")
            return None

    def step_down(self):
        """
        Forces the Vault node to step down from its active status.
        Returns True on success.
        """
        if not self.is_authenticated():
            raise Exception("Vault Client not authenticated.")

        try:
            # step_down doesn't return a body on success, just a 204 status.
            # The hvac library handles this and returns None on success.
            self.client.sys.step_down()  # type: ignore
            # print(f"Successfully requested step-down for Vault node at {self.vault_addr}")
            return True
        except hvac.exceptions.VaultError as e:  # type: ignore
            print(f"Failed to step down Vault node at {self.vault_addr}: {e}")
            return False

    def get_kv_version(self, mount_point="secret"):
        if not self.is_authenticated():
            raise Exception("Vault Client not authenticated.")

        # Check cache first
        if mount_point in self.kv_version_cache:
            return self.kv_version_cache[mount_point]

        mounts = self.client.sys.list_mounted_secrets_engines()["data"]  # type: ignore
        mount_config = mounts.get(f"{mount_point}/")

        if mount_config and mount_config["type"] == "generic":
            self.kv_version_cache[mount_point] = 1
            return 1
        elif not mount_config or mount_config["type"] != "kv":
            raise ValueError(f"No KV engine mounted at '{mount_point}'")

        options = mount_config.get("options", {})
        version = int(options.get("version", 1))

        # Store in cache before returning
        self.kv_version_cache[mount_point] = version
        return version

    def list_all_secret_paths(self, base_path=""):
        if not self.is_authenticated():
            raise Exception("Vault Client not authenticated.")
        all_paths = []
        try:
            response = self.client.secrets.kv.list_secrets(path=base_path)  # type: ignore
            keys = response["data"]["keys"]
            for key in keys:
                full_path = (
                    f"{base_path}{key}" if base_path == "" else f"{base_path}/{key}"
                )
                if key.endswith("/"):
                    all_paths.extend(self.list_all_secret_paths(full_path.rstrip("/")))
                else:
                    all_paths.append(full_path)
        except Exception as e:
            print(f"Failed to list path '{base_path}' for {self.vault_addr}: {e}")
        return all_paths

    def read_secret_path(self, base_path):
        if not self.is_authenticated():
            raise Exception("Vault Client not authenticated.")
        secret = None

        try:
            version = self.get_kv_version()

            if version == 1:
                secret = self.client.secrets.kv.v1.read_secret(path=base_path)  # type: ignore
                return secret.get("data") if secret else None

            elif version == 2:
                secret = self.client.secrets.kv.v2.read_secret_version(  # type: ignore
                    path=base_path, raise_on_deleted_version=True
                )
                return secret["data"]["data"]

        except hvac.exceptions.InvalidPath:  # type: ignore
            return None

    def update_secret_path(self, base_path, secret):
        if not self.is_authenticated():
            raise Exception("Vault Client not authenticated.")
        response = None

        try:
            version = self.get_kv_version()

            if version == 1:
                response = self.client.secrets.kv.v1.create_or_update_secret(  # type: ignore
                    path=base_path, secret=secret
                )
                return response
            elif version == 2:
                response = self.client.secrets.kv.v2.create_or_update_secret(  # type: ignore
                    path=base_path, secret=secret
                )
                return response

        except hvac.exceptions.InvalidPath:  # type: ignore
            return None

    def take_raft_snapshot(self):
        if not self.is_authenticated():
            raise Exception("Vault Client not authenticated.")
        return self.client.sys.raft.take_raft_snapshot().content  # type: ignore

    def restore_raft_snapshot(self, snapshot):
        if not self.is_authenticated():
            raise Exception("Vault Client not authenticated.")
        return self.client.sys.raft.restore_raft_snapshot(snapshot)  # type: ignore
