import os
import logging
import requests
from typing import Optional, Dict, Any

PULSAR_ADMIN_ENDPOINT = os.getenv("PULSAR_ADMIN_ENDPOINT", "http://localhost:8080")
PULSAR_ADMIN_API = f"{PULSAR_ADMIN_ENDPOINT}/admin/v2"
PULSAR_LOG_LEVEL = os.getenv("PULSAR_LOG_LEVEL", "info")

numeric_level = getattr(logging, PULSAR_LOG_LEVEL.upper(), None)
if not isinstance(numeric_level, int):
    raise ValueError("Invalid Log Level: %s", PULSAR_LOG_LEVEL)
logging.basicConfig(
    level=numeric_level,
    format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S",
)
logger = logging.getLogger(__name__)

class PulsarAdminClient:
    def __init__(self, admin_api: Optional[str] = None):
        self.admin_api = admin_api or PULSAR_ADMIN_API
        self.session = requests.Session()

    def _url(self, path: str) -> str:
        return f"{self.admin_api}{path}"

    def create_topic(self, tenant: str, namespace: str, topic: str) -> Any:
        url = self._url(f"/persistent/{tenant}/{namespace}/{topic}")
        logger.info(f"Creating topic: {url}")
        resp = self.session.put(url)
        resp.raise_for_status()
        return resp.json() if resp.content else None

    def delete_topic(self, tenant: str, namespace: str, topic: str, force: bool = False) -> Any:
        url = self._url(f"/persistent/{tenant}/{namespace}/{topic}")
        params = {"force": "true"} if force else {}
        logger.info(f"Deleting topic: {url} (force={force})")
        resp = self.session.delete(url, params=params)
        resp.raise_for_status()
        return resp.json() if resp.content else None

    def set_topic_metadata(self, tenant: str, namespace: str, topic: str, metadata: Dict[str, str]) -> Any:
        url = self._url(f"/persistent/{tenant}/{namespace}/{topic}/metadata")
        logger.info(f"Setting metadata for topic: {url}")
        resp = self.session.post(url, json=metadata)
        resp.raise_for_status()
        return resp.json() if resp.content else None

    def get_topic_metadata(self, tenant: str, namespace: str, topic: str) -> Any:
        url = self._url(f"/persistent/{tenant}/{namespace}/{topic}/metadata")
        logger.info(f"Getting metadata for topic: {url}")
        resp = self.session.get(url)
        resp.raise_for_status()
        return resp.json()

    def list_topics(self, tenant: str, namespace: str) -> Any:
        url = self._url(f"/persistent/{tenant}/{namespace}")
        logger.info(f"Listing topics in namespace: {url}")
        resp = self.session.get(url)
        resp.raise_for_status()
        return resp.json()

# Singleton instance
PulsarAdmin = PulsarAdminClient()
