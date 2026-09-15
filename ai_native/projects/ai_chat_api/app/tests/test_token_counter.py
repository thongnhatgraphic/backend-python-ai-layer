from app.dependencies.token_counter_dependency import counter


def test_token_counter():
    stc1 = "Tôi đang xây dựng một AI Chat API bằng FastAPI."
    stc2 = "I am building an AI Chat API with FastAPI."
    number_of_tokens_sentence_1 = counter.count(text=stc1)

    number_of_tokens_sentence_2 = counter.count(text=stc2)

    print("\n number_of_tokens_sentence_1 \n", number_of_tokens_sentence_1, len(stc1))
    print("\n number_of_tokens_sentence_2 \n", number_of_tokens_sentence_2, len(stc2))


def test_sum(list_tokens: list[int]):
    sum_token = sum([i for i in list_tokens])
    print("\n sum_token \n", sum_token)


test_sum([1, 2, 3, 4, 5])
