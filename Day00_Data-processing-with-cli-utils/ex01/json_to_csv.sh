#/bin/sh

if [ -z "$1" ]
  then
    INPUT_FILE="../ex00/hh.json"  # default
  else
    INPUT_FILE="$1"               # argument
fi

OUTPUT_FILE=hh.csv

FILTER_FILE=filter.jq

cat $INPUT_FILE | jq -r -f $FILTER_FILE > $OUTPUT_FILE