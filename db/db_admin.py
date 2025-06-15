import logging

from .dao import *
from common.dto import *
from datetime import datetime

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("db_admin")

engine = create_engine("sqlite:///db/vending_machine.db")
Session = sessionmaker(bind=engine)


def get_all_products():
    logger.info("get_all_products")
    try:
        with Session() as session:
            product_list = session.query(Product).all()
            return product_list
    except Exception as e:
        logger.error(f"get_all_products Exception: {e}", exc_info=True)
        return {"result": "error", "message": str(e)}


def get_all_orders():
    logger.info("get_all_orders")
    try:
        with Session() as session:
            orders = (
                session.query(
                    Order,
                    case((Order.payment_type == "CASH", "현금"), else_="카드").label(
                        "payment_type_kr"
                    ),
                    case((Receipt.id != None, "Y"), else_="N").label("has_receipt"),
                )
                .outerjoin(Receipt, Receipt.order_id == Order.id)
                .all()
            )

            order_list = []
            for order, payment_type_kr, has_receipt in orders:
                order_list.append(
                    {
                        "id": order.id,
                        "product_name": order.product.name,
                        "company_name": order.product.company_name,
                        "order_at": (
                            order.order_at.strftime("%Y-%m-%d %H:%M:%S")
                            if order.order_at
                            else ""
                        ),
                        "payment_type": payment_type_kr,
                        "cash_amount": order.cash_amount,
                        "cash_change": order.cash_change,
                        "card_info": order.card_info,
                        "has_receipt": has_receipt,
                    }
                )

            return order_list
    except Exception as e:
        logger.error(f"get_all_orders Exception: {e}", exc_info=True)
        return {"result": "error", "message": str(e)}


def update_product(product: ProductData):
    logger.debug("update_product")
    try:
        with Session() as session:
            db_product = session.query(Product).filter_by(id=product.product_id).first()
            if not db_product:
                return {"result": "error", "message": "Product not found"}

            db_product.name = product.product_name
            db_product.stock = product.stock
            db_product.price = product.price
            db_product.company_name = product.company_name
            db_product.kcal = product.kcal
            db_product.caffeine = product.caffeine
            db_product.carbon_acid = product.carbon_acid
            logger.debug(f"carbon_acid to save: {db_product.carbon_acid}")

            db_product.sugar = product.sugar
            db_product.image_path = product.image_path
            db_product.edited_at = datetime.now()

            logger.debug(f"edited_at to save: {db_product.edited_at}")

            session.commit()
            return {"result": "ok", "product_id": db_product.id}
    except Exception as e:
        logger.error(f"update_product Exception: {e}", exc_info=True)
        return {"result": "error", "message": "Unexpected error occurred: " + str(e)}
