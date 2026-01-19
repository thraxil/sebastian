# GEMINI.md

This file provides a summary of useful commands for this project, derived from the `Makefile`.

## Development

*   `make runserver`: Run the Django development server.
*   `make shell`: Open the Django shell.
*   `make install`: Set up the development database for the first time.

## Testing and Linting

*   `make test`: Run the test suite.
*   `make fulltest`: Run tests, checks, and formatting.
*   `make ruff-format`: Format the code using Ruff.
*   `make ruff-check`: Check the code for linting errors with Ruff.
*   `make mypy`: Run MyPy for type checking.
*   `make check`: Run Django's system check.

## Database

*   `make migrate`: Apply database migrations.
*   `make makemigrations`: Create new database migrations.

## Dependencies

*   `make uv.lock`: Lock Python dependencies using `uv`.
*   `make flake.lock`: Update the Nix flake lock file.
*   `make libyear`: Check for outdated dependencies.

## Git workflows

*   `make pull`: Pull changes from git remote, and then run `check`, `test`, and `migrate`.
*   `make rebase`: Pull changes with rebase from git remote, and then run `check`, `test`, and `migrate`.

## Deployment

*   `make collectstatic`: Collect static files for production.

## Cleanup

*   `make clean`: Remove temporary files and directories.
