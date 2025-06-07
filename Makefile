APP=sebastian

all: fulltest

flake.lock: flake.nix
	nix flake update

test: uv.lock
	uv run -- manage.py test

fulltest: uv.lock check ruff-format mypy
	uv run -- manage.py test

uv.lock: pyproject.toml
	uv lock

runserver: check
	uv run -- manage.py runserver

migrate: check
	uv run -- manage.py migrate

makemigrations: check
	uv run -- manage.py makemigrations

check: uv.lock
	uv run -- manage.py check

shell: check
	uv run -- manage.py shell

ruff-format: ruff-check
	uv run -- ruff format $(APP)

ruff-check:
	uv run -- ruff check --select I --fix $(APP)

mypy:
	uv run -- mypy $(APP)

clean:
	rm -rf .venv
	rm -rf static/CACHE
	rm -rf reports
	rm celerybeat-schedule
	rm .coverage
	find . -name '*.pyc' -exec rm {} \;

pull:
	git pull
	make check
	make test
	make migrate

rebase:
	git pull --rebase
	make check
	make test
	make migrate

collectstatic: check
	uv run -- manage.py collectstatic --noinput --settings=$(APP).settings_production

# run this one the very first time you check
# this out on a new machine to set up dev
# database, etc. You probably *DON'T* want
# to run it after that, though.
install: check test
	createdb $(APP)
	uv run -- manage.py syncdb --noinput
	make migrate

.PHONY: clean collectstatic compress install pull rebase shell check migrate runserver test jenkins
