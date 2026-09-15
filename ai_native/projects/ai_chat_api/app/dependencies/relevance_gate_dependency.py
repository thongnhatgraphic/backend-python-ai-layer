from app.services.releven_gate_service import RelevanceGate
from app.core.settings import settings

threshold = settings.RAG_RELEVANCE_THRESHOLD


def get_relevance_gate() -> RelevanceGate:
    return RelevanceGate(threshold)
