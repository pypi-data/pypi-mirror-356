import importlib


def test_dummy():
    assert True


def test_import():
    """Import our newly created module, through importlib to avoid parsing issues"""
    cli = importlib.import_module("accounts_api_client.cli")
    assert hasattr(cli, "main")
