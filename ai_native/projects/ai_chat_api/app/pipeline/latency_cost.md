Backend AI / AI Agent / RAG Engineer:

| Kiến thức                           | Mức cần thiết |
| ----------------------------------- | ------------- |
| Biết model inference là bottleneck  | 🔴 Rất cần    |
| Biết benchmark latency / throughput | 🔴 Rất cần    |
| Biết CPU vs GPU                     | 🔴 Rất cần    |
| Biết batch inference                | 🔴 Rất cần    |
| Biết model size ảnh hưởng resource  | 🔴 Rất cần    |
| Biết threading cơ bản               | 🟠 Nên biết   |
| Biết quantization là gì             | 🟠 Nên biết   |

tests/
    benchmark_reranker.py 
    benchmark_jina_reranker.py
    benchmark_reranker_threads.py

Measure ( đo lường )
   ↓
Profile 
   ↓
Identify bottleneck ( xác định điểm nghẽn )
   ↓
Optimize
   ↓
Benchmark again


Ví dụ sau này gặp:

Reranker = 1.5s CPU

Bạn phải biết những lựa chọn:
K giảm?
Batch?
Threads?
Quantization?
Model nhỏ hơn?
GPU?
ONNX?
Model serving?