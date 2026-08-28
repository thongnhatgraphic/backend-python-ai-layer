import json
from collections import Counter
from pathlib import Path

BASE_DIR = Path(__file__).parent

CORPUS_PATH = BASE_DIR / "corpus.jsonl"
QUERIES_PATH = BASE_DIR / "queries.jsonl"
QRELS_PATH = BASE_DIR / "qrels" / "test.tsv"


def load_jsonl_ids(path: Path) -> set[str]:
    ids: set[str] = set()

    with path.open("r", encoding="utf-8") as f:
        for line in f:
            row = json.loads(line)
            ids.add(str(row["_id"]))

    return ids


def load_qrels(path: Path):
    query_to_docs: dict[str, set[str]] = {}

    with path.open("r", encoding="utf-8") as f:
        next(f)  # skip header

        for line in f:
            query_id, corpus_id, score = line.strip().split("\t")

            if int(score) <= 0:
                continue

            query_to_docs.setdefault(query_id, set()).add(corpus_id)

    return query_to_docs


def main():
    corpus_ids = load_jsonl_ids(CORPUS_PATH)
    query_ids = load_jsonl_ids(QUERIES_PATH)
    qrels = load_qrels(QRELS_PATH)

    print("Corpus documents:", len(corpus_ids))
    print("Queries:", len(query_ids))
    print("Evaluation queries:", len(qrels))

    relevant_doc_ids = {doc_id for docs in qrels.values() for doc_id in docs}

    print("Relevant documents in qrels:", len(relevant_doc_ids))

    missing_docs = relevant_doc_ids - corpus_ids
    missing_queries = set(qrels) - query_ids

    print("Missing corpus ids:", len(missing_docs))
    print("Missing query ids:", len(missing_queries))

    distribution = Counter(len(docs) for docs in qrels.values())

    print("\nRelevant documents per query:")
    for count, frequency in sorted(distribution.items()):
        print(f"{count} relevant docs -> " f"{frequency} queries")


if __name__ == "__main__":
    main()
