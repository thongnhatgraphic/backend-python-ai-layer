from datetime import date
from pydantic import BaseModel, Field, ValidationError, field_validator, model_validator
from typing import Literal


class Booking(BaseModel):
    room_number: int
    check_in_date: date
    check_out_date: date

    @field_validator("room_number")
    @classmethod
    def check_room(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("Số phòng không hợp lệ")
        return v

    @model_validator(mode="after")
    def check_dates(self) -> "Booking":
        if self.check_out_date <= self.check_in_date:
            raise ValueError("Ngày check out phải lớn hơn ngày check in")

        return self


def test_booking(**kwargs):
    try:
        return Booking(**kwargs)
    except ValidationError as e:
        print(e.json())


test_booking(
    room_number=2, check_in_date=date(2023, 1, 2), check_out_date=date(2023, 1, 1)
)

# ticket_book1 = Booking(
#     room_number=0,
#     check_in_date=date(2023, 1, 1),
#     check_out_date=date(2023, 1, 2),
# )

# ticket_book2 = Booking(
#     room_number=1,
#     check_in_date=date(2023, 1, 2),
#     check_out_date=date(2023, 1, 1),
# )
