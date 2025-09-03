[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3120/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Pyright](https://img.shields.io/badge/pyright-checked-informational.svg)](https://github.com/microsoft/pyright/)
[![CI/CD Pipeline](https://github.com/musashimiyomoto/auth-service/actions/workflows/ci.yml/badge.svg)](https://github.com/musashimiyomoto/auth-service/actions/workflows/ci.yml)

------------------------------------------------------------------------

# Auth Service

## Requirements

- Python 3.11
- Poetry
- Docker and Docker Compose

## Quick Start with Makefile

This project includes a comprehensive Makefile that simplifies common development tasks. To see all available commands:

```bash
make help
```

### Docker Run

1. **Build and start the application**:
```bash
make build
```
This command will:
- Automatically copy `.env.example` to `.env` if it doesn't exist
- Build and start the application using Docker Compose

2. **Stop the application**:
```bash
make stop
```

3. **Access the API documentation**:
   - Swagger UI: http://localhost:8000/docs
   - MailCatcher (for testing): http://localhost:1080
   - Adminer (for database): http://localhost:8080

## Development

### Setup

1. **Install all dependencies and setup pre-commit hooks**:
```bash
make install
```
This command will:
- Install all project dependencies including development and test dependencies
- Set up pre-commit hooks for code quality

### Available Makefile Commands

| Command | Description |
|---------|-------------|
| `make help` | Show all available commands with descriptions |
| `make install` | Install dependencies and setup pre-commit hooks |
| `make format` | Format code using black and isort |
| `make check` | Run code quality checks with ruff and pyright |
| `make test` | Run tests with coverage reporting |
| `make build` | Build and start the application with Docker Compose |
| `make stop` | Stop the Docker Compose services |

### Development Workflow

1. **Initial setup**:
```bash
make install
```

2. **Before committing code**:
```bash
make format    # Format your code
make check     # Run linting and type checks
make test      # Run tests
```

3. **Build and test the application**:
```bash
make build     # Start the application
# Test your changes
make stop      # Stop when done
```

## Registration Process

The authentication service implements a secure email verification flow:

1. **User Registration**: User sends a POST request to `/auth/register` with email, password, and optional name fields
2. **Email Verification Code**: After registration, the user sends a POST request to `/auth/send/{email}/code` to receive a verification code
3. **Code Delivery**: The verification code is sent to the user's email and can be accessed via MailCatcher at http://localhost:1080 (for testing purposes)
4. **Email Verification**: User submits the code via POST request to `/auth/verify/{email}/{code}` to verify their account
5. **Account Activation**: Upon successful verification, the user account is activated and they can proceed to login
6. **Authentication**: User can now login via POST request to `/auth/login` and perform authenticated requests
