import os

from .keys import INTEGRATION_KEYS, DB_CONFIG_KEYS, INTERNAL_KEYS
from .secret_manager import SecretManager
from ..common.error import ConfigError


class ConfigService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigService, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.file_path = "secret/db_secret.json"
        return

    def get_db_config(self):
        if os.getenv("PYTHON_ENV") == "DEV":
            db_url = os.getenv(f"{DB_CONFIG_KEYS.DB_URL.value}")
            return db_url
        else:
            secret = SecretManager()
            creds = secret.get_secret_postgres_db()
            return creds

    def get_odoo_config(self):
        odoo_db = self._get_value(INTEGRATION_KEYS.ODOO_DB.value)
        odoo_password = self._get_value(INTEGRATION_KEYS.ODOO_PASSWORD.value)
        odoo_username = self._get_value(INTEGRATION_KEYS.ODOO_USERNAME.value)
        odoo_url = self._get_value(INTEGRATION_KEYS.ODOO_URL.value)
        return {
            "odoo_username": odoo_username,
            "odoo_password": odoo_password,
            "odoo_db": odoo_db,
            "odoo_url": odoo_url,
        }

    def get_mercado_config(self):
        return self._get_value(INTEGRATION_KEYS.MP_ACCESS_TOKEN.value)

    def get_open_ai_config(self):
        return self._get_value(INTEGRATION_KEYS.OPEN_AI_API_KEY.value)

    def get_interbanking_config(self):
        api_client = self._get_value(INTEGRATION_KEYS.INTERBANKING_API_CLIENT.value)
        api_key = self._get_value(INTEGRATION_KEYS.INTERBANKING_API_KEY.value)
        service_url = self._get_value(INTEGRATION_KEYS.INTERBANKING_SERVICE_URL.value)

        return {
            "ib_api_client": api_client,
            "ib_api_key": api_key,
            "ib_service_url": service_url,
        }

    def get_tenant_service_config(self):
        tenant_service_url = self._get_value(INTERNAL_KEYS.TENANT_SERVICE_URL.value)

        return {
            "tenant_service_url": tenant_service_url,
        }
    
    def get_open_ai_config(self):
        open_ai_api_key = self._get_value(INTEGRATION_KEYS.OPEN_AI_API_KEY.value)
        return {
            "open_ai_api_key": open_ai_api_key,
        }

    def _get_value(self, key: str, throw_on_missing=True) -> str:
        value = os.environ.get(f"{key}")
        if not value and throw_on_missing:
            raise ConfigError(f"{key} environment variable is not set")
        return value
