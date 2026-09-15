$ head -n 2 qrels/test.tsv

Output:
query-id        corpus-id       score
1               31715818        1

----------------------------------------------------------

% Lấy ra query _id = 1
$ grep '"_id": "1"' queries.jsonl
Output:
{"_id": "1", "text": "0-dimensional biomaterials show inductive properties.", "metadata": {}}

----------------------------------------------------------

<!-- Tìm _id relevent ứng với query _id = 1 -->
grep '^1[[:space:]]' qrels/test.tsv
Output:
1       31715818        1