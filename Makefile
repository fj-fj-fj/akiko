.DEFAULT_GOAL: all

style:
	flake8 .

grep-review-code:
	./find_flaws.sh

security:
	make grep-review-code

precommit:
	pre-commit run --all-files

.PHONY: all
all:
	make precommit security
