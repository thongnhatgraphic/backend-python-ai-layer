from sqlmodel import Session

from app.core.settings import settings
from app.eval.retrieval.scifact_retriever import (
    engine,
    search,
)

QUERY = "0-dimensional biomaterials show inductive properties."


if __name__ == "__main__":
    with Session(engine) as session:
        results = search(
            session=session,
            query=QUERY,
            limit=50,
        )

        # for rank, row in enumerate(results, start=1):

        #     print(
        #         rank,
        #         str(ground_truth) == str(row.external_id),
        #         row.external_id,
        #         row.score,
        #         row.title,
        #     )
