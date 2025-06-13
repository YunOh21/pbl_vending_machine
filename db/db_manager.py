from .dao import *
from common.dto import *
from datetime import datetime

engine = create_engine("sqlite:///db/vending_machine.db")
Session = sessionmaker(bind=engine)


def get_all_products():
    with Session() as session:
        product_list = session.query(Product).all()
        return product_list


def get_one_product(product_id):
    with Session() as session:
        product = session.query(Product).filter_by(id=product_id).first()
        if not product:
            raise Exception("상품이 존재하지 않습니다.")

        return product


def place_order(order_dto: OrderData):
    with Session() as session:
        product = session.query(Product).filter_by(id=order_dto.product_id).first()
        if not product:
            raise Exception("상품이 존재하지 않습니다.")
        if product.stock <= 0:
            raise Exception("재고가 부족합니다.")

        order_dao = Order(
            product_id=order_dto.product_id,
            payment_type=order_dto.payment_type,
            order_at=datetime.now(),
            card_info=order_dto.card_info,
            cash_amount=order_dto.input_cash_amount,
            cash_change=order_dto.change,
        )
        session.add(order_dao)
        product.stock -= 1
        session.commit()
        return order_dao.id


def get_ordered_product(order_id):
    with Session() as session:
        order = session.query(Order).filter_by(id=order_id).first()
        if not order:
            raise Exception("주문이 존재하지 않습니다.")

        return order.product_id
