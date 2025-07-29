import logging
import requests
from typing import List, Dict, Optional
from ..common.fonder_error import FonderError
from ..config.config_service import ConfigService


class TenantService:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.tenant_url = (
            ConfigService().get_tenant_service_config().get("tenant_service_url")
        )

    def _handle_response(self, response):
        data = response.json()
        if not response.ok:
            self.logger.error(f"Error: {data.get('message')}")
            raise FonderError(f"Error: {data.get('message')}")
        return data

    def get_countries(self):
        # TODO: implement
        pass

    def get_tenants(self) -> List[Dict]:
        self.logger.info(f"Getting tenants from {self.tenant_url}")
        response = requests.get(
            f"{self.tenant_url}/tenants-service/admin-tenants/tenantids"
        )
        return self._handle_response(response)

    def get_tenant_by_id(self, tenant_id: str) -> Dict:
        self.logger.info(f"Getting tenant with id {tenant_id} from {self.tenant_url}")
        response = requests.get(
            f"{self.tenant_url}/tenant-service/admin-tenants/{tenant_id}"
        )
        data = response.json()

        if data.get("statusCode") == 404:
            self.logger.error(f"Tenant not found: {data.get('message')}")
            raise FonderError(
                f"Tenant not found: {data.get('message')}",
                extra={"code": 404, "data": tenant_id},
            )
        elif data.get("statusCode") == 500:
            self.logger.error(f"Error getting tenant: {data.get('message')}")
            raise FonderError(f"Error getting tenant: {data.get('message')}")
        return data

    def get_tenant_by_api_key(self, tenant_api_key: str) -> Dict:
        self.logger.info(
            f"Getting tenant with tenant api key {tenant_api_key} from {self.tenant_url}"
        )
        headers = {"Content-Type": "application/json", "tenant-api-key": tenant_api_key}
        response = requests.get(
            f"{self.tenant_url}/tenants-service/tenants", headers=headers
        )
        return self._handle_response(response)

    def get_tenant_organizations(self, tenant_api_key: str) -> List[Dict]:
        self.logger.info(
            f"Getting organizations for tenant with api key {tenant_api_key}"
        )
        headers = {"Content-Type": "application/json", "tenant-api-key": tenant_api_key}
        response = requests.get(
            f"{self.tenant_url}/tenant-service/tenants/organizations", headers=headers
        )
        return self._handle_response(response)

    def get_tenant_organization(self, tenant_id: str, organization_id: str) -> Dict:
        self.logger.info(
            f"Getting organization {organization_id} for tenant {tenant_id}"
        )
        response = requests.get(
            f"{self.tenant_url}/tenant-service/tenants/{tenant_id}/organizations/{organization_id}",
            headers={"Content-Type": "application/json"},
        )
        return self._handle_response(response)

    def get_banks(self) -> List[Dict]:
        self.logger.info(f"Getting banks from {self.tenant_url}")
        response = requests.get(
            f"{self.tenant_url}/tenant-service/banks",
            headers={"Content-Type": "application/json"},
        )
        return self._handle_response(response)

    def get_bank_by_id(self, bank_id: str) -> Dict:
        self.logger.info(f"Getting bank with id {bank_id}")
        response = requests.get(
            f"{self.tenant_url}/tenant-service/banks/{bank_id}",
            headers={"Content-Type": "application/json"},
        )
        return self._handle_response(response)

    def get_bank_by_code(self, bank_code: str) -> Dict:
        self.logger.info(f"Getting bank with code {bank_code}")
        response = requests.get(
            f"{self.tenant_url}/tenant-service/banks/codes/{bank_code}",
            headers={"Content-Type": "application/json"},
        )
        return self._handle_response(response)

    def get_erps(self) -> List[Dict]:
        self.logger.info(f"Getting ERPs from {self.tenant_url}")
        response = requests.get(
            f"{self.tenant_url}/tenant-service/erps",
            headers={"Content-Type": "application/json"},
        )
        return self._handle_response(response)

    def get_erp_by_id(self, erp_id: str) -> Dict:
        self.logger.debug(f"Getting ERP with id {erp_id}")
        response = requests.get(
            f"{self.tenant_url}/tenant-service/erps/{erp_id}",
            headers={"Content-Type": "application/json"},
        )
        return self._handle_response(response)
