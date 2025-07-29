# src/easy_acumatica/contacts.py
from typing import Any, Dict, Optional
from .client import AcumaticaClient

class ContactsService:
    def __init__(self, client: AcumaticaClient):
        self._client = client

    def get_contacts(self, api_version: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """
        Fetch the list of contacts.
        `params` can include filters like ?$filter=…
        """
        url = f"{self._client.base_url}/entity/Default/{api_version}/Contact"
        resp = self._client.session.get(url, params=params, verify=self._client.verify_ssl)
        resp.raise_for_status()
        return resp.json()