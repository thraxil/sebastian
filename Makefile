APP=sebastian
RUNNER ?= uv run --

all: fulltest

flake.lock: flake.nix
	nix flake update

test: uv.lock
	$(RUNNER) python manage.py test

fulltest: uv.lock check ruff-format mypy
	$(RUNNER) python manage.py test

uv.lock: pyproject.toml
	uv lock

runserver: check
	$(RUNNER) python manage.py runserver

migrate: check
	$(RUNNER) python manage.py migrate

makemigrations: check
	$(RUNNER) python manage.py makemigrations

check: uv.lock
	$(RUNNER) python manage.py check

shell: check
	$(RUNNER) python manage.py shell

ruff-format: ruff-check
	$(RUNNER) ruff format $(APP)

ruff-check:
	$(RUNNER) ruff check --select I --fix $(APP)

mypy:
	$(RUNNER) mypy $(APP)

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

.PHONY: libyear
libyear:
	uvx --from pylibyear==0.3.4 --with typing-extensions libyear toml pyproject.toml
