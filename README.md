[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Pyright](https://img.shields.io/badge/pyright-checked-informational.svg)](https://github.com/microsoft/pyright/)
[![CI/CD Pipeline](https://github.com/musashimiyomoto/restaurant-api/actions/workflows/ci.yml/badge.svg?branch=master)](https://github.com/musashimiyomoto/restaurant-api/actions/workflows/ci.yml)

------------------------------------------------------------------------

# Restaurant Backend

## Prerequisites

- **Docker & Docker Compose** - for containerized development
- **Poetry** - for local development and dependency management

## Quick Start

The fastest way to get started is using our unified development script:

```bash
# Make script executable (first time only)
chmod +x dev.sh

# Run full development cycle: format code, run tests, and build Docker
./dev.sh

# Or run specific operations:
./dev.sh format  # Format code with isort and black
./dev.sh test    # Run tests with pytest
./dev.sh build   # Build and run Docker Compose

# Database migrations:
./dev.sh migrate generate "Add user table"   # Generate new migration
./dev.sh migrate upgrade                     # Apply all pending migrations
./dev.sh migrate downgrade                   # Rollback last migration
./dev.sh migrate history                     # Show migration history
./dev.sh migrate current                     # Show current migration
```

## Setup

1. Clone the repository
2. Create environment file:
   ```bash
   cp .env.example .env
   ```
3. Install dependencies:
   ```bash
   poetry install --with dev,test
   ```

## Docker Development (Recommended)

### Starting the Application

```bash
# Using development script (recommended)
./dev.sh build

# Or manually
docker-compose up --build
```

### Accessing Services

After successful launch:
- **API**: http://localhost:8000
- **DB UI**: http://localhost:8080
  - System: PostgreSQL
  - Server: db
  - Username: postgres
  - Password: postgres
  - Database: restoranchiki
- **Redis UI**: http://localhost:5540
  - Connection string: redis:6379

### Docker Commands

```bash
# Stop all services
docker-compose down

# Rebuild and start
docker-compose up --build

# View logs
docker-compose logs -f api

# Execute commands in running container
docker-compose exec api bash
```

## Local Development

### Database Migrations

The development script automatically handles environment switching for migrations:

```bash
# Generate new migration
./dev.sh migrate generate "Add user table"

# Apply all pending migrations
./dev.sh migrate upgrade

# Show migration history
./dev.sh migrate history

# Show current migration
./dev.sh migrate current

# Rollback last migration
./dev.sh migrate downgrade

# Rollback to specific migration or base
./dev.sh migrate downgrade base
```

### Code Formatting

```bash
# Using development script
./dev.sh format

# Or manually
poetry run isort .
poetry run black .
```

### Running Tests

```bash
# Using development script
./dev.sh test

# Or manually
poetry run pytest -v

# Run specific test file
poetry run pytest tests/test_api/test_admin/ -v
```
