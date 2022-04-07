#/bin/sh

# settings
if [ -z "$1" ]
  then
    INPUT_FILE="../ex03/hh_positions.csv" # default
  else
    INPUT_FILE="$1"                       # argument
fi

OUTPUT_FILE="hh_uniq_positions.csv"


# pass headers
echo '"name","count"' > $OUTPUT_FILE

# clean up
cat $INPUT_FILE \
  | awk 'BEGIN{FS=OFS=",";} NR>1 {print $3;}' \
  | sort \
  | uniq -c \
  | awk 'BEGIN{OFS=","} {print $2, $1;}' \
  >> $OUTPUT_FILE