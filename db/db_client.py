from datetime import datetime

from .dao import *
from .rec_processor import get_rec_query_by_type

from common.dto import *
from common.logger import LoggerManager

logger = LoggerManager.get_logger()

engine = create_engine("sqlite:///db/vending_machine.db")
Session = sessionmaker(bind=engine)


def get_all_products():
    try:
        with Session() as session:
            product_list = session.query(Product).all()
            return product_list
    except Exception as e:
        logger.error(f"get_all_products Exception: {e}", exc_info=True)
        return None


def get_one_product(product_id):
    try:
        with Session() as session:
            product = session.query(Product).filter_by(id=product_id).first()
            if not product:
                logger.warning("상품이 존재하지 않습니다.")
                return None
            return product
    except Exception as e:
        logger.error(f"get_one_product Exception: {e}", exc_info=True)
        return None


def get_rec_product(rec_type):
    try:
        with Session() as session:
            base_query = session.query(Product)
            rec_query = get_rec_query_by_type(rec_type, base_query)
            product = rec_query.first()
            return product
    except Exception as e:
        logger.error(f"get_rec_product Exception: {e}", exc_info=True)
        return None


def insert_order(order_dto: OrderData):
    try:
        with Session() as session:
            product = session.query(Product).filter_by(id=order_dto.product_id).first()
            if not product:
                logger.warning("상품이 존재하지 않습니다.")
                return None
            if product.stock <= 0:
                logger.warning("재고가 부족합니다.")
                return None

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
    except Exception as e:
        try:
            session.rollback()
        except Exception as rollback_e:
            logger.error(
                f"insert_order rollback Exception: {rollback_e}", exc_info=True
            )
        logger.error(f"insert_order Exception: {e}", exc_info=True)
        return None


def get_ordered_product(order_id):
    try:
        with Session() as session:
            order = session.query(Order).filter_by(id=order_id).first()
            if not order:
                logger.warning("주문이 존재하지 않습니다.")
                return None
            return order.product_id
    except Exception as e:
        logger.error(f"get_ordered_product Exception: {e}", exc_info=True)
        return None


def insert_receipt(order_id):
    try:
        with Session() as session:
            receipt_dao = Receipt(order_id=order_id)
            session.add(receipt_dao)
            session.commit()
            return receipt_dao.id
    except Exception as e:
        try:
            session.rollback()
        except Exception as rollback_e:
            logger.error(
                f"insert_receipt rollback Exception: {rollback_e}", exc_info=True
            )
        logger.error(f"insert_receipt Exception: {e}", exc_info=True)
        return None
