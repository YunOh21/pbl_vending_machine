from .dao import *


engine = create_engine("sqlite:///db/vending_machine.db")
Session = sessionmaker(bind=engine)


def get_all_products():
    with Session() as session:
        product_list = session.query(Product).all()
        return product_list


def get_all_orders():
    with Session() as session:
        order_list = session.query(Order).all()
        return order_list
