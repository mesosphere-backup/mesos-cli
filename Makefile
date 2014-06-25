
.PHONY: test
test:
	python setup.py nosetests

.PHONY: clean
clean:
	rm -rf *.egg
	rm -rf .tox
