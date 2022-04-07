["id", "created_at", "name", "has_test", "alternate_url"] as $cols

| .items
| map(. as $row | $cols | map($row[.])) as $rows
| $cols, $rows[]
| @csv