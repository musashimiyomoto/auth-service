[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Pyright](https://img.shields.io/badge/pyright-checked-informational.svg)](https://github.com/microsoft/pyright/)
[![CI/CD Pipeline](https://github.com/musashimiyomoto/auth-service/actions/workflows/ci.yml/badge.svg)](https://github.com/musashimiyomoto/auth-service/actions/workflows/ci.yml)

------------------------------------------------------------------------

# Auth Service

## Requirements

- Docker and Docker Compose

## Setup and Running

1. Clone the repository:
```bash
git clone https://github.com/musashimiyomoto/auth-service.git
cd directory-api
```

2. Create an environment file:
```bash
cp .env.example .env
```

3. Edit the `.env` file with your settings.

4. Start the application with Docker Compose:
```bash
docker compose up --build
```

5. Access the API documentation:
   - Swagger UI: http://localhost:8000/docs

## Registration Process

The authentication service implements a secure email verification flow:

1. **User Registration**: User sends a POST request to `/auth/register` with email, password, and optional name fields
2. **Email Verification Code**: After registration, the user sends a POST request to `/auth/send/{email}/code` to receive a verification code
3. **Code Delivery**: The verification code is sent to the user's email and can be accessed via MailCatcher at http://localhost:1080 (for testing purposes)
4. **Email Verification**: User submits the code via POST request to `/auth/verify/{email}/{code}` to verify their account
5. **Account Activation**: Upon successful verification, the user account is activated and they can proceed to login
6. **Authentication**: User can now login via POST request to `/auth/login` and perform authenticated requests
