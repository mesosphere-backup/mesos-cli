.PHONY: test
env:
	bin/env.sh
test:
	bin/test.sh
.PHONY: fix-isort
fix-isort:
	isort -rc .

.PHONY: clean
clean:
	rm -rf *.egg
	rm -rf .tox
	rm -rf build
	find . -name "*.pyc" -delete
