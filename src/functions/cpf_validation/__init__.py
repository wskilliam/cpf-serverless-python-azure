import azure.functions as func
import pydantic
from pycpfcnpj import cpfcnpj

from src.core.models.http_models import CPFRequest, CPFResponse
from src.core.utils.logger import get_logger
from src.core.utils.rate_limiter import is_rate_limited

logger = get_logger(__name__)

def main(req: func.HttpRequest) -> func.HttpResponse:
    # Rate limiting check
    client_ip = req.headers.get("X-Forwarded-For", "").split(",")[0].strip()
    if not client_ip:
        client_ip = "unknown"

    if is_rate_limited(client_ip):
        logger.warning(f"Rate limit exceeded for IP: {client_ip}")
        return func.HttpResponse(
            body='{"message": "Too many requests. Please try again later."}',
            status_code=429,
            mimetype="application/json"
        )

    logger.info(f"CPF validation request received from IP: {client_ip}")
    try:
        # Parse and validate the request body
        req_body = req.get_json()
        cpf_data = CPFRequest(**req_body)

        # Perform CPF validation
        is_valid = cpfcnpj.validate(cpf_data.cpf)
        if is_valid:
            response_model = CPFResponse(
                cpf=cpf_data.cpf,
                is_valid=True,
                message="The provided CPF is valid."
            )
            status_code = 200
        else:
            response_model = CPFResponse(
                cpf=cpf_data.cpf,
                is_valid=False,
                message="The provided CPF is invalid."
            )
            status_code = 400

        return func.HttpResponse(
            response_model.model_dump_json(),
            status_code=status_code,
            mimetype="application/json"
        )

    except pydantic.ValidationError as e:
        logger.error(f"Validation error: {e}")
        return func.HttpResponse(
            body='{"message": "Invalid request body. Ensure you provide a JSON with a \\"cpf\\" field."}',
            status_code=400,
            mimetype="application/json"
        )
    except ValueError:
        # get_json() fails
        logger.error("Invalid JSON format in request body.")
        return func.HttpResponse(
            body='{"message": "Invalid JSON format in request body."}',
            status_code=400,
            mimetype="application/json"
        )
    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e}")
        return func.HttpResponse(
            body='{"message": "An internal server error occurred."}',
            status_code=500,
            mimetype="application/json"
        )
