# Environment Variables and Local Settings

This document explains how to configure local environment variables for this project. We use two primary files for this purpose: `local.settings.json` and `.env`.

## `local.settings.json`

This file is used by the **Azure Functions Core Tools** to configure the local development environment. The settings in this file are not directly loaded into the Python application code via `python-dotenv`, but are passed as environment variables to the function host when you run `func start`.

### Structure

-   `IsEncrypted`: Should be `false` for local development.
-   `Values`: An object containing key-value pairs that become environment variables.
    -   `AzureWebJobsStorage`: Connection string for the Azure Storage Emulator. Set to `"UseDevelopmentStorage=true"` to use the local emulator.
    -   `FUNCTIONS_WORKER_RUNTIME`: Specifies the language runtime. Should be `"python"`.
    -   `APPINSIGHTS_INSTRUMENTATIONKEY`: The instrumentation key for your Application Insights instance. This is required for distributed tracing and monitoring.

### Example `local.settings.json`

```json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "APPINSIGHTS_INSTRUMENTATIONKEY": "your_instrumentation_key_here"
  }
}
```

> **Note:** This file should **not** be committed to version control as it may contain sensitive information. It is already included in the `.gitignore` file.

## `.env` and `.env.example`

For application-specific environment variables that are not directly related to the Azure Functions host, we use a standard `.env` file, loaded by the `python-dotenv` library.

-   `.env.example`: This file is a template that should be committed to the repository. It lists all the environment variables that the application needs to run, but with placeholder or empty values.
-   `.env`: This is your local file where you provide the actual values for the variables listed in `.env.example`. This file should **never** be committed to version control.

### Usage

1.  Copy `.env.example` to a new file named `.env`.
2.  Fill in the required values in your local `.env` file.

### Example `.env.example`

```
# Example application-specific variable
# MY_API_KEY="your_secret_key_here"
```
