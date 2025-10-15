from pydantic import BaseModel, Field

class CPFRequest(BaseModel):
    """
    Represents the request body for CPF validation.
    """
    cpf: str = Field(..., description="The CPF number to be validated.")

class CPFResponse(BaseModel):
    """
    Represents the structured response for a CPF validation request.
    """
    cpf: str
    is_valid: bool
    message: str
