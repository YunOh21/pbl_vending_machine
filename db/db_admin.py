from .dao import *


engine = create_engine("sqlite:///db/vending_machine.db")
Session = sessionmaker(bind=engine)


def get_all_products():
    with Session() as session:
        product_list = session.query(Product).all()
        return product_list


def get_all_orders():
    with Session() as session:
        orders = (
            session.query(
                Order,
                case((Receipt.id != None, "Y"), else_="N").label("has_receipt"),
            )
            .outerjoin(Receipt, Receipt.order_id == Order.id)
            .all()
        )

        order_list = []
        for order, has_receipt in orders:
            order_list.append(
                {
                    "id": order.id,
                    "product_name": order.product.name,
                    "has_receipt": has_receipt,
                }
            )

        return order_list
