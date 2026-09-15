from sqlmodel import Session, create_engine, select

from app.core.settings import settings
from app.dependencies.ollama_dependency import client
from app.models.rag_document_model import RagDocumentModel
from app.services.embedding_service import EmbeddingService

BATCH_SIZE = 100

engine = create_engine(settings.DATABASE_URL)

embedding_service = EmbeddingService(client)


def build_embedding_text(
    document: RagDocumentModel,
) -> str:
    if document.title:
        return f"{document.title}\n{document.content}"

    return document.content


def embed_documents(session: Session) -> None:
    while True:
        documents = session.exec(
            select(RagDocumentModel)
            .where(RagDocumentModel.embedding.is_(None))
            .limit(BATCH_SIZE)
        ).all()

        if not documents:
            break

        texts = [build_embedding_text(document) for document in documents]

        embeddings = embedding_service.batch_embed_texts(texts)

        if len(embeddings) != len(documents):
            raise ValueError("Embedding count does not match document count")

        for document, embedding in zip(
            documents,
            embeddings,
        ):
            document.embedding = embedding
            session.add(document)

        session.commit()

        print(f"Embedded batch: {len(documents)} documents")


if __name__ == "__main__":
    with Session(engine) as session:
        embed_documents(session)
