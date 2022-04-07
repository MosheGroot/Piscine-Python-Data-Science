#/bin/sh

# settings
if [ -z "$1" ]
  then
    INPUT_FILE="../ex02/hh_sorted.csv"  # default
  else
    INPUT_FILE="$1"                     # argument
fi

OUTPUT_FILE="hh_positions.csv"


# pass headers
cat $INPUT_FILE \
  | head -n 1 \
  > $OUTPUT_FILE


# clean up
cat $INPUT_FILE \
  | tail -n +2 \
  | awk \
    'BEGIN{
      FS=OFS="\",";

      Regexes[0] = "[Jj]unior\\+?/?";
      Regexes[2] = "[Mm]iddle\\+?/?";
      Regexes[4] = "[Ss]enior";

    }

    {
      result = "";
      for (i = 0; i < length(Regexes); ++i)
      {
        match($3, Regexes[i]);
        if (RLENGTH > 0) {
          first_char = substr($3, RSTART, 1);
          result = result toupper(first_char) substr($3, RSTART + 1, RLENGTH - 1);
        }
      }

      if (length(result) == 0) {
        $3 = "\"-";
      }
      else {
        $3 = "\"" result;
      }
      
      print;
    }' \
  >> $OUTPUT_FILE