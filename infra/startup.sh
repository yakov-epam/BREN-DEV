#!/bin/sh
uv run alembic upgrade head
cd src && uv run main.py
