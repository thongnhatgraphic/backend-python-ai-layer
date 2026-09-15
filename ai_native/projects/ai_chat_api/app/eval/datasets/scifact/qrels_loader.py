from pathlib import Path

BASE_DIR = Path(__file__).parent
QRELS_PATH = BASE_DIR / "qrels" / "test.tsv"


def load_qrels(
    path: Path,
) -> dict[str, set[str]]:
    qrels: dict[str, set[str]] = {}

    with path.open("r", encoding="utf-8") as file:
        next(file)  # skip header

        for line in file:
            query_id, corpus_id, score = line.strip().split("\t")

            if int(score) <= 0:
                continue

            qrels.setdefault(query_id, set()).add(corpus_id)

    return qrels
