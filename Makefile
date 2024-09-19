REPO=thraxil
APP=sebastian
MAX_COMPLEXITY=4

all: test

flake.lock: flake.nix
	nix flake update

VE ?= ./.venv
MANAGE ?= ./manage.py
FLAKE8 ?= $(VE)/bin/flake8
SYS_PYTHON ?= python3
PIP ?= $(VE)/bin/pip3
SENTINAL ?= $(VE)/sentinal
REQUIREMENTS ?= requirements.txt

TAG ?= latest
IMAGE ?= $(REPO)/$(APP):$(TAG)

MAX_COMPLEXITY ?= 10

jenkins: $(SENTINAL) check test

test: $(REQUIREMENTS)
	tox --parallel

requirements.txt: requirements.in flake.lock
	uv pip compile --generate-hashes --output-file requirements.txt requirements.in

$(SENTINAL): $(REQUIREMENTS)
	rm -rf $(VE)
	$(SYS_PYTHON) -m venv $(VE)
	$(PIP) install wheel
	$(PIP) install --requirement $(REQUIREMENTS)
	touch $(SENTINAL)

runserver: $(SENTINAL) check
	$(VE)/bin/python $(MANAGE) runserver

migrate: $(SENTINAL) check
	$(VE)/bin/python $(MANAGE) migrate

check: $(SENTINAL)
	$(VE)/bin/python $(MANAGE) check

shell: $(SENTINAL)
	$(VE)/bin/python $(MANAGE) shell

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
	$(VE)/bin/python $(MANAGE) collectstatic --noinput --settings=$(APP).settings_production

compress: $(SENTINAL) check
	$(VE)/bin/python $(MANAGE) compress --settings=$(APP).settings_production

# run this one the very first time you check
# this out on a new machine to set up dev
# database, etc. You probably *DON'T* want
# to run it after that, though.
install: $(SENTINAL) check test
	createdb $(APP)
	$(VE)/bin/python $(MANAGE) syncdb --noinput
	make migrate

.PHONY: clean collectstatic compress install pull rebase shell check migrate runserver test jenkins
