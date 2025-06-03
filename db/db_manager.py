from .db_object import *

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


def place_order(product_id, payment_type):
    with Session() as session:
        product = session.query(Product).filter_by(id=product_id).first()
        if not product:
            raise Exception("상품이 존재하지 않습니다.")
        if product.stock <= 0:
            raise Exception("재고가 부족합니다.")

        order = Order(product_id=product_id, payment_type=payment_type)
        session.add(order)
        product.stock -= 1
        session.commit()
        return order.id


def get_ordered_product(order_id):
    with Session() as session:
        order = session.query(Order).filter_by(id=order_id).first()
        if not order:
            raise Exception("주문이 존재하지 않습니다.")

        return order.product_id
