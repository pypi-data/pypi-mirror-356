from ninebit_ciq import NineBitCIQClient
import pytest

def test_client_instantiation():
    client = NineBitCIQClient("https://example.com", "fake-token")
    assert client.base_url == "https://example.com"


def test_hello_prints(capfd):
    client = NineBitCIQClient()
    client.hello("Alice")
    out, _ = capfd.readouterr()
    assert out.strip() == "hello, Alice"
    