.PHONY: all

clean:
	rm -Rf build

build:
	python setup.py sdist

publish: build
	python setup.py upload
