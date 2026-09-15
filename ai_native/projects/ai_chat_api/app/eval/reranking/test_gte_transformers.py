import torch

from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
)

MODEL_NAME = "Alibaba-NLP/gte-multilingual-reranker-base"


def main():

    print("Loading tokenizer...")

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    print("Loading model...")

    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME,
        trust_remote_code=True,
    )

    model.eval()

    query = "0-dimensional biomaterials show inductive properties."

    document = (
        "Biomaterials with specific nanoscale structures "
        "can influence cellular behavior and differentiation."
    )

    inputs = tokenizer(
        query,
        document,
        return_tensors="pt",
        truncation=True,
        max_length=8192,
    )

    print("input_ids shape:", inputs["input_ids"].shape)

    with torch.no_grad():

        outputs = model(**inputs)

    print("logits:", outputs.logits)


if __name__ == "__main__":
    main()
