#/bin/sh

# settings
if [ -z "$1" ]
  then
    OUTPUT_FILE="./hh_positions.csv"  # default
  else
    OUTPUT_FILE="$1"                  # argument
fi

INPUT_DIR="splitted"
INPUT_FILE_PREFIX="created_at_"
INPUT_FILE_EXTENTION=".csv"


# get files (convert it to array)
FILE_LIST=($(ls $INPUT_DIR/$INPUT_FILE_PREFIX*$INPUT_FILE_EXTENTION))

# create output file and insert header
cat ${FILE_LIST[0]} \
  | head -n 1 \
  > $OUTPUT_FILE

# concatenate all files to OUTPUT_FILE
for file in ${FILE_LIST[@]}
do
  cat $file \
    | tail -n +2 \
    >> $OUTPUT_FILE
done
  # >> $OUTPUT_FILE
  # | uniq -c \