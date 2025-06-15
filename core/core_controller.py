from db import db_client
from common.dto import *


def get_all_products():
    return db_client.get_all_products()


def get_one_product(product_id):
    return db_client.get_one_product(product_id)


def place_order(order_dto: OrderData):
    print(f"controller:place_order, order_dto: {order_dto}")
    return db_client.insert_order(order_dto)


def get_ordered_product(order_id):
    return db_client.get_ordered_product(order_id)


def add_receipt(order_id):
    return db_client.insert_receipt(order_id)
