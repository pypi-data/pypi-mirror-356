from pathlib import Path
import requests

class EnvFetchError(Exception):
    pass


class EnvySettingsLoader:
    _env_written = False

    @classmethod
    def load_env_file(
        cls,
        envy_env: str,
        filename: str = ".env.envy",
        encoding: str = "utf-8",
        envy_url: str = "https://environment-api.nextpertise.nl",
        keycloak_url: str = "https://id.nextpertise.nl/realms/identity",
        client_id: str = None,
        client_secret: str = None,
        verify_https_requests: bool = True,
    ) -> None:
        """
        Load environment variables from a remote Envy environment and generate a .env.envy file if it doesn't exist.

        The following parameters configure the fetch and can be overridden by environment variables:
        - envy_env: Environment name to fetch variables for.
        - filename: Output path for the fetched .env file (default: ".env.envy").
        - encoding: Encoding used to write the file (default: "utf-8").
        - envy_url: URL to the Envy environment API (default: "https://environment-api.nextpertise.nl`").
        - keycloak_url: Keycloak base URL (default: "https://id.nextpertise.nl/realms/identity").
        - client_id: Optional. If not provided or in ENVY_KEYCLOAK_CLIENT_ID, will attempt to load from ~/.envy/auth.json.
        - client_secret: Optional. If not provided or in ENVY_KEYCLOAK_TOKEN, will attempt to load from ~/.envy/auth.json.
        - verify_https_requests: Whether to verify HTTPS certificates (default: True).

        Environment variables ENVY_URL, ENVY_KEYCLOAK_URL, ENVY_KEYCLOAK_CLIENT_ID, ENVY_KEYCLOAK_TOKEN,
        ENVY_ENVIRONMENT, and ENVY_VERIFY_HTTPS override the corresponding parameters if set.
        """
        import os

        envy_url = os.getenv("ENVY_URL", envy_url)
        keycloak_url = os.getenv("ENVY_KEYCLOAK_URL", keycloak_url)
        client_id = os.getenv("ENVY_KEYCLOAK_CLIENT_ID", client_id)
        client_secret = os.getenv("ENVY_KEYCLOAK_TOKEN", client_secret)

        if not client_id or not client_secret:
            from pathlib import Path
            import json

            auth_path = Path.home() / ".envy" / "auth.json"

            if auth_path.exists():
                try:
                    with auth_path.open("r", encoding="utf-8") as f:
                        auth_data = json.load(f)
                    client_id = client_id or auth_data.get("client_id")
                    client_secret = client_secret or auth_data.get("client_secret")
                except Exception as e:
                    raise EnvFetchError(f"Failed to load credentials from {auth_path}: {e}")

        envy_env = os.getenv("ENVY_ENVIRONMENT", envy_env)
        verify_https_requests = os.getenv("ENVY_VERIFY_HTTPS", str(verify_https_requests)).strip().lower() in ("1", "true", "yes", "on", True)

        if cls._env_written:
            return
        cls._env_written = True

        env_file_path = Path(filename)

        if env_file_path.exists():
            return

        if not all([envy_url, keycloak_url, client_id, client_secret, envy_env]):
            return  # insufficient config

        try:
            token_url = f"{keycloak_url.rstrip('/')}/protocol/openid-connect/token"
            token_response = requests.post(
                token_url,
                data={
                    "grant_type": "client_credentials",
                    "client_id": client_id,
                    "client_secret": client_secret,
                },
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Accept": "application/json",
                },
                verify=verify_https_requests,
            )
            token_response.raise_for_status()
            access_token = token_response.json().get("access_token")
            if not access_token:
                raise EnvFetchError("Missing access_token")

            response = requests.get(
                f"{envy_url.rstrip('/')}/environments/{envy_env}/variables?with_inherited=true",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "text/plain",
                },
                verify=verify_https_requests,
            )
            response.raise_for_status()
            env_file_path.write_text(response.text, encoding=encoding)

        except (requests.RequestException, EnvFetchError) as e:
            if env_file_path.exists():
                print(f"[envy] Warning: {e}. Using existing {env_file_path}.")
            else:
                raise EnvFetchError(f"Could not fetch remote env and no fallback: {e}")
