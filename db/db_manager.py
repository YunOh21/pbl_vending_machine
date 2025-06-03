from .db_object import *

def get_all():
    engine = create_engine('sqlite:///db/vending_machine.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    product_list = session.query(Product).all()

    session.close()
    return product_list