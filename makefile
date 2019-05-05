help: # print targets and quit
	@perl -ne '/^([A-Za-z0-9-_]+):.*#\s+(.*)/ && \
		printf "%*s%s\n", 10, $$1, $$2 ? " - $$2" : ""' makefile

clean: # remove virtualenv and all build files
	-rm -r .venv
	-rm -r dist
	-rm -r build
	-rm -r $(notdir $(CURDIR)).egg-info

prepare: # set up virtual env
	python3 -m venv .venv
	source .venv/bin/activate && python3 -m pip install setuptools wheel twine

build: # build package
	python3 setup.py bdist_wheel

install: # install package locally
	source .venv/bin/activate && python3 -m pip install dist/*.whl

bump-minor: # increase minor version
	git tag | tail -1 | cut -c2- | perl -pe 's/\d+\.\d+\.\K(\d+)/ $$1+1 /e'

bump-major: # increase major version
	git tag | tail -1 | cut -c2- | perl -pe 's/\d+\.\d+\.\K(\d+)/ $$1+1 /e'

upload: build # upload package to pypi
	python3 -m twine upload dist/*
