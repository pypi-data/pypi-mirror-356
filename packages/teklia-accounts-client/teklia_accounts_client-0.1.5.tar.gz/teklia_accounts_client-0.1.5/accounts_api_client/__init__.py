import logging

from accounts_api_client.client import AccountsClient, License  # noqa: F401

logging.basicConfig(
    format="%(asctime)s %(levelname)s/%(name)s: %(message)s",
    level=logging.INFO,
)
