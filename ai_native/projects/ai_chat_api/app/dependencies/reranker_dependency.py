import torch
from app.services.reranker_service import RerankerService
from transformers import AutoModelForSequenceClassification, AutoTokenizer

MODEL_NAME = "BAAI/bge-reranker-v2-m3"
torch.set_num_threads(12)

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

model.eval()

reranker_service = RerankerService(
    tokenizer=tokenizer,
    model=model,
)


def get_reranker_dependency() -> RerankerService:
    return reranker_service
