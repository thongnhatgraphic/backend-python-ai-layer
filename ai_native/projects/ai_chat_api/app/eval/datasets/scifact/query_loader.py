import json
from pathlib import Path

BASE_DIR = Path(__file__).parent
QRELS_PATH = BASE_DIR / "queries.jsonl"


def load_queries(path: Path):
    queries: dict[str, str] = {}

    with path.open("r", encoding="utf-8") as file:
        for line in file:
            row = json.loads(line)

            query_id = str(row["_id"])
            query_text = row["text"]

            queries[query_id] = query_text

    return queries
