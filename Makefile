.PHONY: prepare install install-all lint package publish-test publish-prod

PROJECT_DIR := mctl

prepare:
	pipx install poetry

install: prepare
	cd $(PROJECT_DIR) && poetry install

install-all:
	cd $(PROJECT_DIR) && poetry install --with dev

lint:
	cd $(PROJECT_DIR) && poetry run pylint src
	cd $(PROJECT_DIR) && poetry run mypy src/mctl

clean:
	cd $(PROJECT_DIR) && poetry env remove --all || true
	rm -rf $(PROJECT_DIR)/dist $(PROJECT_DIR)/.venv

reinstall: clean install

package: install
	cd $(PROJECT_DIR) && poetry check
	cd $(PROJECT_DIR) && poetry build

publish-test: package
	cd $(PROJECT_DIR) && poetry publish -r testpypi --build

publish-prod: package
	cd $(PROJECT_DIR) && poetry publish -r pypi --build
