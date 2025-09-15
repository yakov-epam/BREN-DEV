# Entry project

A books API.

## Assumptions

When implementing this solution, I made a few assumptions, I believe it is important to state them:

- ORM usage would be preferred over plain SQL with a custom connector.
- Partial request implementation for PUT endpoint shouldn't be too complex.
- There should be no "autogens" for better comprehension and lesser complexity, hence the list endpoints are a bit
  "spaghetti".
- Swagger documentation will be used for testing (therefore the app is optimized for it).
- The app will be hosted at AWS (yet I didn't test the Terraform configuration so it might be faulty if you run it).
- A proper testing framework should be used instead of manually running test functions.
- Automated tests will run in CI workflow(s) rather than locally.

> Note: Unfortunately SQLModel library and asynchronous database interaction caused way too many problems,
> so after hours of struggling I gave up and went for a simple yet reliable synchronous setup.

## Prerequisites

- Docker engine with compose plugin (optionally Docker Desktop or similar).
- [uv Python package manager](https://docs.astral.sh/uv/getting-started/installation/) (for running directly only).
- Linux, macOS or WSL.
- A terminal emulator.

## Understanding configuration options

You can find the `.env.example` configuration file under `env/` folder. \
Read through the file and create a `.env` in the same folder.

## Auth

- User:
  - username: `user`
  - password: `useruser`
- Admin:
  - username: `admin`
  - password: `adminadmin`

## Running the app

### With Docker, dev mode

Follow this section to run the app in developer mode in Docker. \
This option gives a hot reload.

1. Run `cd infra`.
2. Run `docker compose up -d --build` (try `docker-compose` if `docker compose` doesn't work).
3. Go to http://localhost:8080/v1/docs for docs.

### With Docker, prod mode

Follow this section to run the app in production mode (using `granian` instead of `uvicorn`) in Docker.

1. Run `cd infra`.
2. Set `ENV=prod` in `env/.env`.
3. Run `docker compose up -d --build` (try `docker-compose` if `docker compose` doesn't work).
4. Go to http://localhost:8080/v1/docs for docs.

> Note: Test user accounts will not be created for prod mode. You will need to seed them to the DB manually.

### Directly

Follow this section if you want to debug the app or develop it further.

1. Follow steps from [With Docker, dev mode](#with-docker-dev-mode) section.
2. Stop the app container.
3. Run `uv sync`.
4. Apply migrations if necessary: `uv run alembic upgrade head`.
5. Optional for speedups: Run `uv sync --group speedups`.
6. Optional for dev tools: Run `uv sync --group dev`.
7. Run `cd src`.
8. Run `uv run main.py`
9. Go to http://localhost:8080/v1/docs for docs.
10. Follow steps from [IDE Setup](#ide-setup-pycharm-example) if necessary.

## IDE Setup (Pycharm example)

1. Configure project interpreter to `uv`, Python version is 3.13.7
2. Follow steps involving `uv sync` from [Running the app directly](#directly), do not skip step 4.
3. Mark `src` folder as `Sources Root`.
4. Run `pre-commit install`.

## Running tests

1. Create `test` database.
2. Update `.env` to use that database.
3. Run `pytest` in project root.
4. Delete `test` database if you feel like so.

## Terraforming

You can find the Terraform guide [here](infra/terraform/README.md).
