import logging
from db import db_client
from common.dto import *


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

logger = logging.getLogger("core_controller")


def get_all_products():
    logger.debug("get_all_products")
    return db_client.get_all_products()


def get_one_product(product_id):
    logger.debug(f"get_one_product, product_id: {product_id}")
    return db_client.get_one_product(product_id)


def get_rec_product(type):
    logger.debug(f"get_rec_product, type: {type}")
    return db_client.get_rec_product(type)


def place_order(order_dto: OrderData):
    logger.debug(f"place_order, order_dto: {order_dto}")
    return db_client.insert_order(order_dto)


def get_ordered_product(order_id):
    logger.debug(f"get_ordered_product, order_id: {order_id}")
    return db_client.get_ordered_product(order_id)


def add_receipt(order_id):
    logger.debug(f"add_receipt, order_id: {order_id}")
    return db_client.insert_receipt(order_id)
