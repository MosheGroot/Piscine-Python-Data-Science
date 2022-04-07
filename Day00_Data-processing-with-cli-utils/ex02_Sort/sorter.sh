#/bin/sh

if [ -z "$1" ]
  then
    INPUT_FILE="../ex01/hh.csv"   # default
  else
    INPUT_FILE="$1"               # argument
fi

OUTPUT_FILE="hh_sorted.csv"


# pass headers
cat $INPUT_FILE \
  | head -n 1 \
  > $OUTPUT_FILE

# sort
cat $INPUT_FILE \
  | tail -n +2 \
  | sort --field-separator=',' --key=2,2 --key=1,1 \
  >> $OUTPUT_FILE