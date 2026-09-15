# Requirement
#     ↓
# Shortlist
#     ↓
# Model A ─────┐
#              │
# Model B ─────┼──→ cùng evaluation dataset
#              │
# Model C ─────┘
#              ↓
# Quality
# Latency
# Cost
# Resource
# License
#              ↓
# Production decision
from transformers import AutoModelForSequenceClassification
import torch
import os

from transformers import AutoModelForSequenceClassification, AutoTokenizer
from app.tests.test_semantic_search import semantic_search, embedding1
from uuid import UUID
import time

torch.get_num_threads()

print("PyTorch threads:", torch.get_num_threads())
print("CPU cores:", os.cpu_count())


# MODEL_NAME = "jinaai/jina-reranker-v2-base-multilingual"
MODEL_NAME = "BAAI/bge-reranker-v2-m3"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_NAME,
    trust_remote_code=True,
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

# Tokenization: 2.93 ms
# Model:        1525.14 ms
# Total:        1528.07 ms

# Tokenization: 1.58 ms
# Model:        1511.17 ms
# Total:        1512.75 ms

# Tokenization: 3.66 ms
# Model:        1483.51 ms
# Total:        1487.16 ms

# Tokenization: 2.03 ms
# Model:        1506.70 ms
# Total:        1508.73 ms

# Tokenization: 2.27 ms
# Model:        1652.50 ms
# Total:        1654.77 ms
