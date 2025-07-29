import os
import logging
import pulsar

PULSAR_ENDPOINT = os.getenv("PULSAR_ENDPOINT", "pulsar://localhost:6650")
PULSAR_ADMIN_ENDPOINT = os.getenv("PULSAR_ADMIN_ENDPOINT", "http://localhost:8080")
PULSAR_IO_THREADS = int(os.getenv("PULSAR_IO_THREADS", "4"))
PULSAR_MESSAGE_LISTENER_THREADS = int(os.getenv("PULSAR_MESSAGE_LISTENER_THREADS", "4"))
PULSAR_CONCURRENT_LOOKUP_REQUEST = int(os.getenv("PULSAR_CONCURRENT_LOOKUP_REQUEST", "50000"))
PULSAR_LOG_LEVEL = os.getenv("PULSAR_LOG_LEVEL", "info")

# Configure pulsar's logger
numeric_level = getattr(logging, PULSAR_LOG_LEVEL.upper(), None)
if not isinstance(numeric_level, int):
    raise ValueError("Invalid Log Level: %s", PULSAR_LOG_LEVEL)
logging.basicConfig(
    level=numeric_level,
    format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S",
)

logger = logging.getLogger(__name__)

class PulsarClientMgr:

    def __init__(self):
        self._client = None

    @property
    def client(self) -> pulsar.Client:
        if self._client is not None:
            return self._client
        
        client = pulsar.Client(
            service_url=PULSAR_ENDPOINT,
            connection_timeout_ms=10000,
            io_threads=PULSAR_IO_THREADS,
            message_listener_threads=PULSAR_MESSAGE_LISTENER_THREADS,
            logger=logger,
            operation_timeout_seconds = 300,
            stats_interval_in_seconds = 600,
            authentication=None, # likely want to revisit
            use_tls = False, # likely want to revisit at some point if we want to legit glue our apps right into pulsar on the frontend. 
        )

        self._client = client

        return self._client


# instantiate here so it operates like a singleton
PulsarClient = PulsarClientMgr()
