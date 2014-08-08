
.PHONY: test
test:
	isort mesos/**/*.py tests/**/*.py -c
	python setup.py flake8 nosetests --where tests

.PHONY: clean
clean:
	rm -rf *.egg
	rm -rf .tox
