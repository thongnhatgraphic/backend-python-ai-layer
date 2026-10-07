from pydantic import BaseModel, Field, computed_field


class OrderItem(BaseModel):
    item_name: str = Field(
        description="The name of the item", min_length=3, max_length=50
    )
    quantity: int = Field(description="The quantity of the item", gt=0)
    price_per_unit: float = Field(description="The price of the item", gt=0)

    @computed_field
    def total_price(self):
        return self.quantity * self.price_per_unit


class Order(BaseModel):
    order_id: str = Field(description="The order ID", min_length=3, max_length=50)
    customer_name: str = Field(
        description="The name of the customer", min_length=3, max_length=50
    )
    items: list[OrderItem]


laptop = OrderItem(
    item_name="Laptop",
    quantity=1,
    price_per_unit=1500,
)

mouse = OrderItem(
    item_name="Mouse",
    quantity=1,
    price_per_unit=15,
)

order = Order(
    order_id="123",
    customer_name="John Doe",
    items=[laptop, mouse],
)

print(order.model_dump_json())
