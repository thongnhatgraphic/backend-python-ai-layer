import json
from pathlib import Path

from sqlmodel import Session, create_engine

from app.models.rag_document_model import RagDocumentModel
from app.core.settings import settings

CORPUS_PATH = (
    Path(__file__).resolve().parents[1] / "datasets" / "scifact" / "corpus.jsonl"
)

engine = create_engine(
    settings.DATABASE_URL,
)

BATCH_SIZE = 100


def ingest_corpus(session: Session):
    batch = []

    with CORPUS_PATH.open(
        "r",
        encoding="utf-8",
    ) as file:
        for line in file:
            row = json.loads(line)

            document = RagDocumentModel(
                external_id=str(row["_id"]),
                title=row.get("title"),
                content=row["text"],
            )

            batch.append(document)

            if len(batch) >= BATCH_SIZE:
                session.add_all(batch)
                session.commit()

                batch.clear()

    # Xử lý phần còn lại
    if batch:
        session.add_all(batch)
        session.commit()


with Session(engine) as session:
    ingest_corpus(session)
