.DEFAULT_GOAL: all

.PHONY: grep-review-code
grep-review-code:
	./find_flaws.sh

.PHONY: security
security:
	make grep-review-code

.PHONY: all
all:
	make security
