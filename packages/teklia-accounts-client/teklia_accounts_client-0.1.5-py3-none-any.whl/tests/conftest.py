import os
from json import dumps as json_dumps
from urllib.parse import urljoin

import pytest
from nacl.encoding import Base64Encoder
from nacl.signing import SigningKey

from accounts_api_client import AccountsClient

BASE_URL = "https://accounts.server"
PRIVATE_KEY = SigningKey(seed=b"a" * 32)
VERIFY_KEY = PRIVATE_KEY.verify_key.encode(encoder=Base64Encoder).decode()


@pytest.fixture(autouse=True)
def _setup_environment(responses):
    """Setup needed environment variables"""

    # Allow accessing remote API schemas
    # defaulting to the prod environment
    schema_url = os.environ.get(
        "ARKINDEX_API_SCHEMA_URL",
        "https://arkindex.teklia.com/api/v1/openapi/?format=openapi-json",
    )
    responses.add_passthru(schema_url)

    # Set schema url in environment
    os.environ["ARKINDEX_API_SCHEMA_URL"] = schema_url

    # Set default signature key
    os.environ["SIGNATURE_PUBLIC_KEY"] = "ytNtv77HFFA9yxd2bc/vsjyj+q+7A/jnEOux6UxcbCw="


@pytest.fixture
def accounts_mocker(responses):
    def _mock(
        path: str,
        method: str = "GET",
        status: int = 200,
        json: dict | None = None,
        headers: dict | None = None,
    ):
        accounts_headers = {
            "Date": "2000-01-01T01:01:01.0000",
            "Digest": "aaaaa",
            "Host": BASE_URL,
            "Request-target": f"{method} {path}",
        }
        payload = json_dumps(
            {k.lower(): v for k, v in accounts_headers.items()},
            indent=4,
            sort_keys=True,
        )
        accounts_headers["Teklia-Signature"] = PRIVATE_KEY.sign(
            payload.encode(), encoder=Base64Encoder
        ).signature.decode()
        responses.add(
            getattr(responses, method),
            urljoin(BASE_URL, path),
            status=status,
            json=json,
            headers={**accounts_headers, **(headers or {})},
        )

    return _mock


@pytest.fixture
def client():
    return AccountsClient(base_url=BASE_URL, verify_key=VERIFY_KEY)
