from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class OrderData:
    product_id: int
    payment_type: str
    input_cash_amount: Optional[int]  # 카드인 경우 null
    card_info: Optional[str]  # 카드사 + 카드번호 마지막 4자리, 현금인 경우 null
    change: Optional[int]  # 카드인 경우 null


@dataclass
class ProductData:
    product_id: str
    product_name: str
    stock: int
    price: int
    company_name: str
    kcal: Optional[int] = None
    caffeine: Optional[int] = None
    carbon_acid: Optional[int] = None
    sugar: Optional[int] = None
    image_path: Optional[str] = None
