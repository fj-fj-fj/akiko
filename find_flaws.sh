#!/bin/bash

# flaw finder static analysis

set -e
set -o pipefail

CONTEXT=1
COLOR="always"
SIGNATURES="./potential_security_flaws"
EXCLUDEFILES="--exclude=.gitignore --exclude=potential_security_flaws"

# -R is recursive
# -H prints the name of the file
# -C prints # lines of context before and after the match
# -E uses extended regexp
# -f specifies the rule file (signatures potential_security_flaws)
# -n prints the line number
grep --color=$COLOR \
    --exclude-dir=.git \
    --exclude-dir=.mypy_cache \
    --exclude-dir=staticfiles \
    --exclude-dir=data \
    --exclude-dir=htmlcov \
    --exclude-dir=reports \
    --exclude-dir=requirements \
    $EXCLUDEFILES \
    -n -R -H -C "$CONTEXT" -E \
    -f "$SIGNATURES" | \
    sed -e"s/$(printf '\r')//g" -e"s/^\(\x1b\[.*m\x1b\[K\)--\(\x1b\[.*\x1b\[K\)$/\1###2/" -e"s/^--$/###/" | \
    sed -e"#" -e"#"

SUCCESS=$?
exit $SUCCESS
