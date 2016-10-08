.PHONY: all

clean:
	rm -Rf build

publish:
	python setup.py sdist upload
