build:
	poetry build

publish:
	poetry publish

# poetry config repositories.testpypi https://test.pypi.org/legacy/
publish-test:
	poetry publish -r testpypi
