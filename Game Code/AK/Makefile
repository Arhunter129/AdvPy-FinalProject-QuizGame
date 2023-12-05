TEST = pytest 
TEST_ARGS = --verbose --color=yes
TYPE_CHECK = mypy --strict
STYLE_CHECK = flake8
STYLE_FIX = autopep8 --in-place --recursive --aggressive --aggressive
KATTIS = python3 kattis-cli/submit.py 

.PHONY: all
all: style-fix style-check type-check unittest clean

.PHONY: style-fix
style-fix:
	$(STYLE_FIX) PyQuizGame_Logic.py

.PHONY: type-check
type-check:
	$(TYPE_CHECK) PyQuizGame_Logic.py

.PHONY: style-check
style-check:
	$(STYLE_CHECK) PyQuizGame_Logic.py

.PHONY: run-test
run-test:
	$(TEST) $(TEST_ARGS) unit_test_PyQuizGame_Logic.py

unittest:
	$(TEST) unit_test_PyQuizGame_Logic.py
	@echo "Unittest done."

.PHONY: clean
clean:
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .hypothesis

.PHONY: push
push: run-test clean
