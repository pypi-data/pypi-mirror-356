import requests_mock
import requests
from slopsquat_detector.validator import is_on_pypi

def test_known_package():
    with requests_mock.Mocker() as m:
        m.get("https://pypi.org/pypi/requests/json", status_code=200)
        assert is_on_pypi("requests") is True

def test_fake_package():
    with requests_mock.Mocker() as m:
        m.get("https://pypi.org/pypi/fake-package-123/json", status_code=404)
        assert is_on_pypi("fake-package-123") is False

def test_network_error():
    with requests_mock.Mocker() as m:
        m.get("https://pypi.org/pypi/error-pkg/json", exc=requests.exceptions.ConnectTimeout)
        assert is_on_pypi("error-pkg") is False