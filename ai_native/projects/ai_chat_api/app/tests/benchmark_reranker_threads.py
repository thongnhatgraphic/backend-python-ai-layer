# ① Vector Search
#         ↓
# ② Candidate K
#         ↓
# ③ Reranking
#         ↓
# ④ Quality evaluation
#         ↓
# ⑤ Latency benchmark
#         ↓
# ⑥ Model comparison
#         ↓
# ⑦ Profiling
#         ↓
# ⑧ CPU threading        ← ĐANG Ở ĐÂY

# Quantization: Lượng tử hoá

import torch
import time
from app.tests.benchmark_jina_reranker import model, inputs

for num_threads in [1, 2, 4, 6, 8, 12]:

    torch.set_num_threads(num_threads)

    # warm-up
    with torch.no_grad():
        model(**inputs, return_dict=True)

    times = []

    for _ in range(5):
        start = time.perf_counter()

        with torch.no_grad():
            model(**inputs, return_dict=True)

        elapsed = time.perf_counter() - start

        times.append(elapsed * 1000)

    avg = sum(times) / len(times)

    print(f"threads={num_threads} " f"avg={avg:.2f} ms")
