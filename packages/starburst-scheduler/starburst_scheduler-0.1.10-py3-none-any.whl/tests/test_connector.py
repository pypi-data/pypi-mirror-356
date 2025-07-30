import pytest
from starburst_scheduler.connector import StarburstConnector

def test_dummy():
    assert 1 + 1 == 2

def test_connector_init():
    connector = StarburstConnector(
        host="test.trino.galaxy.starburst.io",
        port=443,
        user="test@example.com",
        password="testpass",
        catalog="system",
        schema="runtime"
    )
    assert connector.db_parameters["host"] == "test.trino.galaxy.starburst.io"
    assert connector.db_parameters["port"] == 443
    assert connector.db_parameters["catalog"] == "system"
    assert connector.db_parameters["schema"] == "runtime"

def test_connector_connect_fail(mocker):
    mocker.patch('pystarburst.Session.builder.configs', side_effect=Exception("Connection failed"))
    connector = StarburstConnector("test.host", 443, "user", "pass", "catalog", "schema")
    assert not connector.connect()