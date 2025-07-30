import logging

import pytest
import requests

from accounts_api_client.client import (
    AccountsClient,
    AccountsException,
    InvalidSignature,
    License,
    LicenseExpired,
    LicenseInvalid,
    LicenseNotFound,
    ServerError,
)


@pytest.mark.parametrize(
    ("status_code", "expected"),
    [
        (401, LicenseNotFound),
        (402, LicenseExpired),
        (403, LicenseInvalid),
        (404, LicenseNotFound),
        (418, AccountsException),
        (501, ServerError),
    ],
)
def test_get_license_error(monkeypatch, accounts_mocker, client, status_code, expected):
    monkeypatch.setattr("tenacity.nap.time.sleep", lambda x: None)
    accounts_mocker("api/v1/license/", status=status_code)
    with pytest.raises(expected):
        client.get_license(license_key="not_found")


def test_get_license_unexpected_json(accounts_mocker, client):
    accounts_mocker(
        "api/v1/license/",
        json={"status": "AAAA"},
    )
    with pytest.raises(AccountsException):
        client.get_license(license_key="key")


def test_get_license_invalid_signature(accounts_mocker, client):
    accounts_mocker(
        "api/v1/license/",
        json={
            "name": "test",
            "uses": 5,
            "max_uses": 25,
            "status": "ACTIVE",
        },
        headers={"Teklia-Signature": "aaaaaaa"},
    )
    with pytest.raises(InvalidSignature):
        client.get_license(license_key="key")


def test_get_license_invalid_public_key(accounts_mocker):
    accounts_mocker(
        "api/v1/license/",
        json={
            "name": "test",
            "uses": 5,
            "max_uses": 25,
            "status": "ACTIVE",
        },
        headers={"Teklia-Signature": "aaaaaaa"},
    )
    client = AccountsClient(
        base_url="https://accounts.server",
        verify_key="eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHg=",
    )
    with pytest.raises(InvalidSignature):
        client.get_license(license_key="key")


def test_get_license(accounts_mocker, client):
    accounts_mocker(
        "api/v1/license/",
        json={
            "name": "test",
            "uses": 5,
            "max_uses": 25,
            "status": "ACTIVE",
        },
    )
    assert client.get_license(license_key="key") == License(
        key="key",
        name="test",
        status=License.Status.Active,
        uses=5,
        max_uses=25,
    )


@pytest.mark.parametrize(
    ("status_code", "expected"),
    [
        (401, LicenseNotFound),
        (402, LicenseExpired),
        (403, LicenseInvalid),
        (404, LicenseNotFound),
        (418, AccountsException),
        (501, ServerError),
    ],
)
def test_publish_action_error(
    monkeypatch, accounts_mocker, client, status_code, expected
):
    # Patch retry for supported error codes
    monkeypatch.setattr("tenacity.nap.time.sleep", lambda x: None)
    accounts_mocker(
        "api/v1/product/test/action/transcribe/", method="POST", status=status_code
    )
    with pytest.raises(expected):
        client.publish_action(
            license_key="not_found", product_slug="test", action_slug="transcribe"
        )


def test_publish_action_invalid_signature(accounts_mocker, client):
    accounts_mocker(
        "api/v1/product/test/action/transcribe/",
        method="POST",
        headers={"Date": "aaaaaaa"},
    )
    with pytest.raises(InvalidSignature):
        client.publish_action(
            license_key="not_found", product_slug="test", action_slug="transcribe"
        )


def test_publish_action_invalid_public_key(accounts_mocker):
    accounts_mocker("api/v1/product/test/action/transcribe/", method="POST")
    client = AccountsClient(
        base_url="https://accounts.server",
        verify_key="eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHg=",
    )
    with pytest.raises(InvalidSignature):
        client.publish_action(
            license_key="not_found", product_slug="test", action_slug="transcribe"
        )


def test_publish_action(accounts_mocker, client):
    accounts_mocker("api/v1/product/test/action/transcribe/", method="POST")
    assert (
        client.publish_action(
            license_key="not_found", product_slug="test", action_slug="transcribe"
        )
        is None
    )


def test_publish_action_with_license(accounts_mocker, client):
    """license_key parameter is not required once the client is authenticated"""
    accounts_mocker(
        "api/v1/license/",
        json={
            "name": "test",
            "uses": 5,
            "max_uses": 25,
            "status": "ACTIVE",
        },
    )
    accounts_mocker("api/v1/product/test/action/transcribe/", method="POST")
    with pytest.raises(
        AccountsException, match="A license key must be used to perform this action"
    ):
        client.publish_action(product_slug="test", action_slug="transcribe")
    client.get_license(license_key="key")
    client.publish_action(product_slug="test", action_slug="transcribe")


def test_str_value(accounts_mocker, client):
    accounts_mocker(
        "api/v1/license/",
        json={
            "name": "Trial license for tests",
            "uses": 5,
            "max_uses": 25,
            "status": "ACTIVE",
        },
    )
    assert str(client) == "No license checked"
    assert client.get_license(license_key="key")
    assert str(client) == "Trial license for tests"


def test_retry_on_connect_timeout(monkeypatch, responses, client, caplog):
    monkeypatch.setattr("tenacity.nap.time.sleep", lambda x: None)
    responses.add(
        responses.POST,
        f"{client.base_url}/a/",
        body=requests.exceptions.ConnectTimeout(),
    )
    with pytest.raises(requests.exceptions.ConnectTimeout):
        client.request(method="post", path="/a/")
    assert len(responses.calls) == 3
    assert caplog.record_tuples == [
        (
            "accounts_api_client.client",
            logging.INFO,
            "Retrying accounts_api_client.client.AccountsClient.request in 2.0 seconds as it raised ConnectTimeout: .",
        ),
        (
            "accounts_api_client.client",
            logging.INFO,
            "Retrying accounts_api_client.client.AccountsClient.request in 4.0 seconds as it raised ConnectTimeout: .",
        ),
    ]


def test_retry_on_connect_error(monkeypatch, responses, client, caplog):
    monkeypatch.setattr("tenacity.nap.time.sleep", lambda x: None)
    responses.add(
        responses.GET,
        f"{client.base_url}/b/",
        body=requests.exceptions.ConnectionError(),
    )
    with pytest.raises(requests.exceptions.ConnectionError):
        client.request(method="get", path="/b/")
    assert len(responses.calls) == 3
    assert caplog.record_tuples == [
        (
            "accounts_api_client.client",
            logging.INFO,
            "Retrying accounts_api_client.client.AccountsClient.request in 2.0 seconds as it raised ConnectionError: .",
        ),
        (
            "accounts_api_client.client",
            logging.INFO,
            "Retrying accounts_api_client.client.AccountsClient.request in 4.0 seconds as it raised ConnectionError: .",
        ),
    ]


@pytest.mark.parametrize("status_code", [429, 500, 529])
def test_retry_on_http_error(
    monkeypatch, responses, accounts_mocker, client, caplog, status_code
):
    monkeypatch.setattr("tenacity.nap.time.sleep", lambda x: None)
    accounts_mocker(method="PATCH", path="/c/", status=status_code)
    response = client.request(method="patch", path="/c/")
    with pytest.raises(requests.exceptions.HTTPError):
        response.raise_for_status()
    assert len(responses.calls) == 3
    assert caplog.record_tuples == [
        (
            "accounts_api_client.client",
            logging.INFO,
            (
                "Retrying accounts_api_client.client.AccountsClient.request in 2.0 seconds as it returned "
                f"<Response [{status_code}]>."
            ),
        ),
        (
            "accounts_api_client.client",
            logging.INFO,
            (
                "Retrying accounts_api_client.client.AccountsClient.request in 4.0 seconds as it returned "
                f"<Response [{status_code}]>."
            ),
        ),
    ]
