from db import db_admin


def get_all_products():
    return db_admin.get_all_products()


def get_all_orders():
    return db_admin.get_all_orders()
