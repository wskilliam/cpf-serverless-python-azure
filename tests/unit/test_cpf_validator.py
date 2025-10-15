import unittest.mock
import pytest
from pycpfcnpj import cpfcnpj

# Test cases for the cpfcnpj.validate function, which is the core of our CPF validation logic.

@pytest.mark.parametrize("cpf", ["11144477735", "98765432100"]) # Sample valid CPFs
def test_validate_valid_cpf(cpf):
    """Test that cpfcnpj.validate returns True for valid CPFs."""
    assert cpfcnpj.validate(cpf) is True

@pytest.mark.parametrize("cpf", ["11144477700", "12345678901"]) # Sample invalid CPFs
def test_validate_invalid_cpf(cpf):
    """Test that cpfcnpj.validate returns False for invalid CPFs."""
    assert cpfcnpj.validate(cpf) is False

def test_validate_formatted_cpf():
    """Test that cpfcnpj.validate handles formatted CPFs correctly."""
    assert cpfcnpj.validate("111.444.777-35") is True
    assert cpfcnpj.validate("987.654.321-00") is True

@pytest.mark.parametrize("cpf", [
    "11111111111",
    "22222222222",
    "99999999999"
])
def test_validate_repeated_digits_cpf(cpf):
    """Test that cpfcnpj.validate returns False for CPFs with all repeated digits."""
    assert cpfcnpj.validate(cpf) is False

def test_validate_short_cpf():
    """Test that cpfcnpj.validate returns False for CPFs that are too short."""
    assert cpfcnpj.validate("1234567890") is False

def test_validate_long_cpf():
    """Test that cpfcnpj.validate returns False for CPFs that are too long."""
    assert cpfcnpj.validate("123456789012") is False

def test_validate_non_numeric_cpf():
    """Test that cpfcnpj.validate returns False for CPFs with non-numeric characters."""
    assert cpfcnpj.validate("abcdefghijk") is False
