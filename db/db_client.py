import logging
from .dao import *
from common.dto import *
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

engine = create_engine("sqlite:///db/vending_machine.db")
Session = sessionmaker(bind=engine)


def get_all_products():
    try:
        with Session() as session:
            product_list = session.query(Product).all()
            return product_list
    except Exception as e:
        logging.error(f"get_all_products error: {e}", exc_info=True)
        return {"result": "error", "message": str(e)}


def get_one_product(product_id):
    try:
        with Session() as session:
            product = session.query(Product).filter_by(id=product_id).first()
            if not product:
                return {"result": "error", "message": "상품이 존재하지 않습니다."}
            return product
    except Exception as e:
        logging.error(f"get_one_product error: {e}", exc_info=True)
        return {"result": "error", "message": str(e)}


def insert_order(order_dto: OrderData):
    try:
        with Session() as session:
            product = session.query(Product).filter_by(id=order_dto.product_id).first()
            if not product:
                return {"result": "error", "message": "상품이 존재하지 않습니다."}
            if product.stock <= 0:
                return {"result": "error", "message": "재고가 부족합니다."}

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
            return {"result": "ok", "order_id": order_dao.id}
    except Exception as e:
        logging.error(f"insert_order error: {e}", exc_info=True)
        return {"result": "error", "message": str(e)}


def get_ordered_product(order_id):
    try:
        with Session() as session:
            order = session.query(Order).filter_by(id=order_id).first()
            if not order:
                return {"result": "error", "message": "주문이 존재하지 않습니다."}
            return {"result": "ok", "product_id": order.product_id}
    except Exception as e:
        logging.error(f"get_ordered_product error: {e}", exc_info=True)
        return {"result": "error", "message": str(e)}


def insert_receipt(order_id):
    try:
        with Session() as session:
            receipt_dao = Receipt(order_id=order_id)
            session.add(receipt_dao)
            session.commit()
            return {"result": "ok", "receipt_id": receipt_dao.id}
    except Exception as e:
        logging.error(f"insert_receipt error: {e}", exc_info=True)
        return {"result": "error", "message": str(e)}
