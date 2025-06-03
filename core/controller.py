from db import db_manager


def get_all_products():
    return db_manager.get_all_products()


def get_one_product(product_id):
    return db_manager.get_one_product(product_id)


def place_order(product_id, payment_type):
    return db_manager.place_order(product_id, payment_type)


def get_ordered_product(order_id):
    return db_manager.get_ordered_product(order_id)
