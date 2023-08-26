.PHONY: remove_local
remove_local:
	git remote update --prune
	git switch --detach origin/main
	@git for-each-ref --format '%(refname:short)' refs/heads | xargs -r -t git branch -D

.PHONY: install_test
install_test:
	poetry install --no-root --without dev,publish

.PHONY: install_publish
install_publish:
	poetry install --no-root --without dev,test

.PHONY: test
test:
	poetry run pytest -s

.PHONY: publish
publish:
	poetry run python -m build
	poetry run twine upload dist/*