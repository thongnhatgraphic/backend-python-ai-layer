FP32
               │
               ▼
         BGE Reranker
               │
          12 CPU threads
               │
               ▼
          ~1270 ms

Ta tạo:

              INT8
               │
               ▼
         BGE Reranker
               │
          12 CPU threads
               │
               ▼
              ?

Sau đó đo:
    Quality
    Latency
    Model size

| Version | Precision@5 | Recall@5 | Latency |
| ------- | ----------: | -------: | ------: |
| FP32    |        1.0* |     1.0* | ~1270ms |
| INT8    |           ? |        ? |       ? |


Performance thực tế phụ thuộc:
    CPU instruction support
    runtime
    model architecture
    memory bandwidth
    implementation
    batch size