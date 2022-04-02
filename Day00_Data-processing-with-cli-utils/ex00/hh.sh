#!/bin/sh

OUTPUT_FILE="./hh.json"
VACANCY_AMOUNT="100"

VACANCY_NAME="${1/ /+}"

curl -k -H 'User-Agent: api-test-agent' -G "https://api.hh.ru/vacancies?text=$VACANCY_NAME&per_page=$VACANCY_AMOUNT" | jq > $OUTPUT_FILE
