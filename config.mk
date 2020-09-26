# default config values that can all be overridden
VE ?= ./ve
MANAGE ?= ./manage.py
FLAKE8 ?= $(VE)/bin/flake8
SYS_PYTHON ?= python3
PIP ?= $(VE)/bin/pip3
SENTINAL ?= $(VE)/sentinal
REQUIREMENTS ?= requirements.txt

JS_FILES ?= media/js/
TAG ?= latest
IMAGE ?= $(REPO)/$(APP):$(TAG)

MAX_COMPLEXITY ?= 10

