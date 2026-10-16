#!/bin/sh
set -e

# Execute the migrations of database
uv run alembic upgrade head

# start the application
uv run uvicorn fast_zero.app:app --host 0.0.0.0 --port 8000