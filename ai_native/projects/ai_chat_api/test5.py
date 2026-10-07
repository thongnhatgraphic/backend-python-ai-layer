from typing import Annotated

list_msg = [1, 2, 3, 4, 5]

last_msg = list_msg[-1]

print(last_msg)

# 1. Định nghĩa các kiểu dữ liệu kèm metadata
USD = Annotated[float, {"currency": "USD", "rate_to_usd": 1.0}]
VND = Annotated[float, {"currency": "VND", "rate_to_usd": 25000.0}]
EUR = Annotated[float, {"currency": "EUR", "rate_to_usd": 0.92}]


# 2. Hàm quy đổi đọc trực tiếp từ tham số truyền vào
def convert_currency(amount: float, from_type, to_type) -> float:
    # Không dùng get_type_hints() nữa, truy cập thẳng vào kiểu dữ liệu truyền vào
    from_meta = from_type.__metadata__[0]
    print("from_meta", from_meta)
    to_meta = to_type.__metadata__[0]
    print("to_meta", to_meta)

    amount_in_usd = amount / from_meta["rate_to_usd"]
    result = amount_in_usd * to_meta["rate_to_usd"]

    print(f"Chuyển đổi từ {from_meta['currency']} sang {to_meta['currency']}:")
    return round(result, 2)


# ---- RUN ----
money_in_vnd = 500000.0
ket_qua = convert_currency(money_in_vnd, from_type=VND, to_type=EUR)

print(f"Input: {money_in_vnd} VND")
print(f"Output: {ket_qua} EUR")
