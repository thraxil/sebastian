REPO=thraxil
APP=sebastian
MAX_COMPLEXITY=4

all: test

flake.lock: flake.nix
	nix flake update

VE ?= ./ve
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

coverage: $(SENTINAL)
	. $(VE)/bin/activate && $(VE)/bin/coverage run --source='$(APP)' $(MANAGE) test \
	&& $(VE)/bin/coverage html -d reports --omit='*migrations*,*settings_*,*wsgi*'

requirements.txt: requirements.in flake.lock
	uv pip compile --generate-hashes --output-file requirements.txt requirements.in

$(SENTINAL): $(REQUIREMENTS)
	rm -rf $(VE)
	$(SYS_PYTHON) -m venv $(VE)
	$(PIP) install wheel
	$(PIP) install --requirement $(REQUIREMENTS)
	touch $(SENTINAL)

runserver: $(SENTINAL) check
	$(MANAGE) runserver

migrate: $(SENTINAL) check
	$(MANAGE) migrate

check: $(SENTINAL)
	$(MANAGE) check

shell: $(SENTINAL)
	$(MANAGE) shell_plus

clean:
	rm -rf ve
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
	$(MANAGE) collectstatic --noinput --settings=$(APP).settings_production

compress: $(SENTINAL) check
	$(MANAGE) compress --settings=$(APP).settings_production

# run this one the very first time you check
# this out on a new machine to set up dev
# database, etc. You probably *DON'T* want
# to run it after that, though.
install: $(SENTINAL) check test
	createdb $(APP)
	$(MANAGE) syncdb --noinput
	make migrate

.PHONY: clean collectstatic compress install pull rebase shell check migrate runserver test jenkins
ROOT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

