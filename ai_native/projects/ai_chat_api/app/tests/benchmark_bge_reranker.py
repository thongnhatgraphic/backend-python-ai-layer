from transformers import AutoModelForSequenceClassification
import torch
import os

from transformers import AutoModelForSequenceClassification, AutoTokenizer
from app.tests.test_semantic_search import semantic_search, embedding1
from uuid import UUID
import time

NUM_THREADS = 12
torch.set_num_threads(NUM_THREADS)

print("PyTorch threads:", torch.get_num_threads())
print("CPU cores:", os.cpu_count())

MODEL_NAME = "BAAI/bge-reranker-v2-m3"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_NAME,
)
model.eval()

candidates = semantic_search(
    UUID("43371a56-0d6b-454a-87c9-5c78b593122b"),
    embedding1,
    limit=19,
)
query = "Tôi đang học Python"

pairs = [[query, memory.memory.content] for memory in candidates[:15]]
# print("pairs", pairs)
with torch.no_grad():
    # torch.set_num_threads(NUM_THREADS)
    # print("PyTorch threads after :", torch.get_num_threads())
    # print("CPU cores:", os.cpu_count())

    # 1. Tokenization
    start = time.perf_counter()

    inputs = tokenizer(
        pairs,
        padding=True,
        truncation=True,
        return_tensors="pt",
        max_length=512,
    )

    tokenize_elapsed = time.perf_counter() - start

    # 2. Model inference
    start = time.perf_counter()

    scores = model(**inputs, return_dict=True).logits.view(-1).float()

    inference_elapsed = time.perf_counter() - start

    print(f"Tokenization: {tokenize_elapsed * 1000:.2f} ms")
    print(f"Model:        {inference_elapsed * 1000:.2f} ms")
    print(f"Total:        " f"{(tokenize_elapsed + inference_elapsed) * 1000:.2f} ms")

    # results = sorted(
    #     zip(pairs, scores.tolist()),
    #     key=lambda x: x[1],
    #     reverse=True,
    # )

    # for pair, score in results:
    #     print(score, pair[1])

    # print(f"Reranker inference: {elapsed * 1000:.2f} ms")
    # print(scores)
