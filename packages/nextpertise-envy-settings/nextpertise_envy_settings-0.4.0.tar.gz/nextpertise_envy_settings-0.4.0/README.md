# nextpertise-envy-loader

A reusable helper for Pydantic that fetches environment variables from an Envy API using a Keycloak-secured token. It automatically writes these variables to a `.env.envy` file and prepends it to your environment configuration.

---

## 📦 Installation

Install via Poetry:

```bash
poetry add nextpertise-envy-settings
```

Or with pip:

```bash
pip install nextpertise-envy-settings
```

⸻

## 🚀 Usage

To load your environment configuration into a `.env.envy` file:

```python
from nextpertise_envy_settings import EnvySettingsLoader

EnvySettingsLoader.load_env_file(
    envy_env="SCORE_DEVELOPMENT"
)
```

This will:

- Check for required settings in environment variables (or fall back to defaults).
- Load `client_id` and `client_secret` from environment or `~/.envy/auth.json` if not passed explicitly.
- Fetch remote settings from the configured Envy environment.
- Write them to `.env.envy` in the current directory.

### Optional overrides

You can override default URLs or encoding directly:

```python
EnvySettingsLoader.load_env_file(
    envy_env="SCORE_DEVELOPMENT",
    envy_url="https://custom-envy.example.com",
    keycloak_url="https://keycloak.example.com/realms/envy",
    filename=".env.generated",
    encoding="utf-8"
)
```

> ✅ If `client_id` and `client_secret` are not passed or set in environment variables, they are loaded from `~/.envy/auth.json`.

⸻

🔧 Environment Variables (optional)

Instead of hardcoding the config, you can also use these environment variables:

| Variable                        | Description               |
|---------------------------------|---------------------------|
| `ENV_API_BASE_URL`              | Base URL for Envy API     |
| `ENV_API_KEYCLOAK_URL`          | Keycloak realm URL        |
| `ENV_API_KEYCLOAK_CLIENT_ID`    | OAuth2 client ID          |
| `ENV_API_KEYCLOAK_TOKEN`        | OAuth2 client secret      |
| `ENV_API_ENVIRONMENT`           | Target environment name   |


⸻

📁 Example .env.envy

MYSQL_USER=abc
MYSQL_PASSWORD=xyz
REDIS_HOST=localhost
