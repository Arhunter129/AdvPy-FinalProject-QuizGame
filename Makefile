GAME = gamecode/flaskrender.py
MAIN = mongo_to_txt.py
TESTMAIN = test_mongo_to_text.py
PY = python3

all: demo check_style fix_style check_types unittest clean
	@echo "All tests passed!"

unittest:
ifeq ($(shell which pytest), )
	@echo "pytest not found. Installing..."
	pip install pytest
endif
	pytest -v $(TESTMAIN)

check_style:
	flake8 $(MAIN) --count --show-source --statistics
	flake8 $(TESTMAIN) --count --show-source --statistics

fix_style:
	autopep8 --in-place --recursive --aggressive --aggressive $(MAIN)
	autopep8 --in-place --recursive --aggressive --aggressive $(TESTMAIN)

check_types:
	mypy --disallow-untyped-defs --strict $(MAIN)
	mypy --disallow-untyped-defs --strict $(TESTMAIN)

demo:
	$(PY) $(GAME)

clean:
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf .mypy_cache