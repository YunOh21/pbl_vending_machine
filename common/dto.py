from dataclasses import dataclass

@dataclass
class OrderData:
    product_id: int
    payment_type: str
    input_cash_amount: int  # 카드인 경우 null
    card_info: str          # 카드사 + 카드번호 마지막 4자리, 현금인 경우 null
    change: int             # 카드인 경우 null