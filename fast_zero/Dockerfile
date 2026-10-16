# Dockerfile for FastAPI application using uv
FROM python:3.13-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Config uv
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_NO_DEV=1

# Copy archives and dependencies
COPY pyproject.toml uv.lock ./

# Install dependencies without installing the project
RUN uv sync --frozen --no-install-project

# Copy the application code
COPY . .

# Install the project
RUN uv sync --frozen

# Run the application
CMD ["uv", "run", "uvicorn", "fast_zero.app:app", "--host", "0.0.0.0", "--port", "8000"]