APP=sebastian
all: test

flake.lock: flake.nix
	nix flake update

MANAGE ?= ./manage.py
SENTINAL ?= .venv/bin/activate

jenkins: $(SENTINAL) check test

test: uv.lock
	tox --parallel

uv.lock: pyproject.toml
	uv lock

$(SENTINAL): uv.lock
	test -d .venv || uv venv .venv
	VIRTUAL_ENV=.venv uv pip install -r pyproject.toml

runserver: $(SENTINAL) check
	.venv/bin/python $(MANAGE) runserver

migrate: $(SENTINAL) check
	.venv/bin/python $(MANAGE) migrate

check: $(SENTINAL)
	.venv/bin/python $(MANAGE) check

shell: $(SENTINAL)
	.venv/bin/python $(MANAGE) shell

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

collectstatic: $(SENTINAL) check
	.venv/bin/python $(MANAGE) collectstatic --noinput --settings=$(APP).settings_production

compress: $(SENTINAL) check
	.venv/bin/python $(MANAGE) compress --settings=$(APP).settings_production

# run this one the very first time you check
# this out on a new machine to set up dev
# database, etc. You probably *DON'T* want
# to run it after that, though.
install: $(SENTINAL) check test
	createdb $(APP)
	.venv/bin/python $(MANAGE) syncdb --noinput
	make migrate

.PHONY: clean collectstatic compress install pull rebase shell check migrate runserver test jenkins
