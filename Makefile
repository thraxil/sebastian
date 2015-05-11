MANAGE=./manage.py
APP=sebastian
FLAKE8=./ve/bin/flake8

test: ./ve/bin/python
	$(MANAGE) test

./ve/bin/python: requirements.txt bootstrap.py virtualenv.py
	./bootstrap.py

flake8: ./ve/bin/python
	$(FLAKE8) $(APP) --max-complexity=10

runserver: ./ve/bin/python validate
	$(MANAGE) runserver

migrate: ./ve/bin/python validate
	$(MANAGE) migrate

validate: ./ve/bin/python
	$(MANAGE) validate

shell: ./ve/bin/python
	$(MANAGE) shell_plus

build:
	docker build -t thraxil/sebastian .

clean:
	rm -rf ve
	rm -rf media/CACHE
	rm -rf reports
	rm celerybeat-schedule
	rm .coverage
	find . -name '*.pyc' -exec rm {} \;

pull:
	git pull
	make validate
	make test
	make migrate
	make flake8

rebase:
	git pull --rebase
	make validate
	make test
	make migrate
	make flake8

collectstatic: ./ve/bin/python validate
	$(MANAGE) collectstatic --noinput --settings=$(APP).settings_production

compress: ./ve/bin/python validate
	$(MANAGE) compress --settings=$(APP).settings_production

# run this one the very first time you check
# this out on a new machine to set up dev
# database, etc. You probably *DON'T* want
# to run it after that, though.
install: ./ve/bin/python validate test
	createdb $(APP)
	$(MANAGE) syncdb --noinput
	make migrate
