#/bin/sh

# settings
if [ -z "$1" ]
  then
    INPUT_FILE="../ex03/hh_positions.csv" # default
  else
    INPUT_FILE="$1"                       # argument
fi

OUTPUT_DIR="splitted"
OUTPUT_FILE_PREFIX="created_at_"
OUTPUT_FILE_EXTENTION=".csv"

# get dates
UNIQUE_DATES=$(cat $INPUT_FILE \
                | tail -n +2 \
                | awk 'BEGIN{FS=",\""} {split($2, result, "T"); print result[1];}' \
                | sort \
                | uniq \
              )


mkdir -p $OUTPUT_DIR
for date in $UNIQUE_DATES
do
  CURRENT_FILE="$OUTPUT_DIR/$OUTPUT_FILE_PREFIX$date$OUTPUT_FILE_EXTENTION"
  touch $CURRENT_FILE
  
  cat $INPUT_FILE \
    | head -n 1 \
    > $CURRENT_FILE

  cat $INPUT_FILE \
    | tail -n +2 \
    | awk -v date=$date \
      'BEGIN{FS=OFS=","}
      {
        i = index($2, date);
        if (i > 0)
        {
          print $0;
        }
      }' \
    >> $CURRENT_FILE
done
  # >> $OUTPUT_FILE
  # | uniq -c \