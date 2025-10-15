# Local Development Guide

This guide provides instructions on how to set up and run this Azure Functions project on your local machine for development and testing.

## Prerequisites

Before you begin, ensure you have the following installed:

1.  **Python 3.8+** (managed with `pyenv` is recommended).
2.  **Poetry** for dependency management.
3.  **Azure Functions Core Tools v4**.
4.  **Azurite**, the local Azure Storage emulator.

Refer to the main `README.md` for detailed installation instructions for the tools above. For Azurite, you can install it globally via npm:

```bash
npm install -g azurite
```

## Running the Project Locally

### 1. Start the Storage Emulator

Before running the function, you need to start the Azurite storage emulator. Open a dedicated terminal and run:

```bash
azurite
```

This will emulate the Azure Storage services (Blob, Queue, Table) that the Azure Functions host requires.

### 2. Install Dependencies

If you haven't already, install the project dependencies using Poetry:

```bash
poetry install
```

### 3. Run the Function App

We have provided a convenient script to start the local development server with hot-reload enabled. In your project's root directory, run:

```bash
./scripts/start-local.sh
```

This will start the Azure Functions host. The output will show you the URL where your function is running, typically `http://localhost:7071`.

## Testing the Endpoint Manually

You can test the `validate-cpf` endpoint using a tool like `curl`.

### Example 1: Valid CPF

```bash
curl -X POST \
  http://localhost:7071/api/validate-cpf \
  -H 'Content-Type: application/json' \
  -d '{"cpf": "11144477735"}'
```

**Expected Response (HTTP 200):**

```json
{
  "cpf": "11144477735",
  "is_valid": true,
  "message": "The provided CPF is valid."
}
```

### Example 2: Invalid CPF

```bash
curl -X POST \
  http://localhost:7071/api/validate-cpf \
  -H 'Content-Type: application/json' \
  -d '{"cpf": "11111111111"}'
```

**Expected Response (HTTP 400):**

```json
{
  "cpf": "11111111111",
  "is_valid": false,
  "message": "The provided CPF is invalid."
}
```

### Example 3: Malformed Request (Missing Field)

```bash
curl -X POST \
  http://localhost:7071/api/validate-cpf \
  -H 'Content-Type: application/json' \
  -d '{"document": "12345"}'
```

**Expected Response (HTTP 400):**

```json
{
  "message": "Invalid request body. Ensure you provide a JSON with a \"cpf\" field."
}
```
