import pytest
import json
from src.functions.cpf_validation import main

@pytest.fixture
def create_mock_request():
    from azure.functions import HttpRequest
    import urllib

    def _make_request(method="POST", url="/api/validate-cpf", body=None, headers=None):
        headers = headers or {"Content-Type": "application/json"}
        if body is not None and isinstance(body, dict):
            body = json.dumps(body)
        return HttpRequest(
            method=method,
            url=url,
            body=body.encode("utf-8") if body else b"",
            headers=headers,
            params=urllib.parse.parse_qs("")
        )
    return _make_request

def test_valid_cpf_returns_200(create_mock_request):
    body = {"cpf": "11144477735"}
    req = create_mock_request(body=body)
    resp = main(req)
    assert resp.status_code == 200
    data = json.loads(resp.get_body())
    assert data["is_valid"] is True

def test_invalid_cpf_returns_400(create_mock_request):
    body = {"cpf": "12345678900"}
    req = create_mock_request(body=body)
    resp = main(req)
    assert resp.status_code == 400
    data = json.loads(resp.get_body())
    assert data["is_valid"] is False

def test_missing_cpf_returns_400(create_mock_request):
    body = {}
    req = create_mock_request(body=body)
    resp = main(req)
    assert resp.status_code == 400
    assert b"cpf" in resp.get_body() or b"Invalid request body" in resp.get_body()

def test_invalid_json_returns_400(create_mock_request):
    req = create_mock_request(body="cpf=notjson", headers={"Content-Type": "application/json"})
    resp = main(req)
    assert resp.status_code == 400

def test_rate_limited_returns_429(monkeypatch, create_mock_request):
    monkeypatch.setattr("src.functions.cpf_validation.is_rate_limited", lambda ip: True)
    body = {"cpf": "11144477735"}
    req = create_mock_request(body=body)
    resp = main(req)
    assert resp.status_code == 429
    data = json.loads(resp.get_body())
    assert "Too many requests" in data["message"]

def test_unexpected_exception(monkeypatch, create_mock_request):
    # força um erro interno no CPFRequest (ex: quebra proposital)
    monkeypatch.setattr("src.functions.cpf_validation.CPFRequest", lambda *a, **kw: (_ for _ in ()).throw(Exception("fail")))
    body = {"cpf": "11144477735"}
    req = create_mock_request(body=body)
    resp = main(req)
    assert resp.status_code == 500
    assert b"internal" in resp.get_body().lower()
