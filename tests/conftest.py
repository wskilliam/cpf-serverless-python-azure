import json
import azure.functions as func
import pytest

@pytest.fixture
def create_mock_request():
    """Factory to create a mock HttpRequest for testing."""
    def _create(body: dict = None, headers: dict = None) -> func.HttpRequest:
        """Creates a mock HttpRequest for testing."""
        req_body_bytes = b''
        if body is not None:
            req_body_bytes = json.dumps(body).encode('utf-8')

        # If headers are not provided at all, use the default with an IP.
        # If an empty dict `{}` is passed, it will be used, simulating no headers.
        if headers is None:
            headers = {'X-Forwarded-For': '127.0.0.1'}

        return func.HttpRequest(
            method="POST",
            url="/api/validate-cpf",
            headers=headers,
            body=req_body_bytes
        )
    return _create
