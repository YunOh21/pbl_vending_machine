from .db_object import *
    
    
def main():
    engine = create_engine('sqlite:///db/vending_machine.db')
    Base.metadata.create_all(engine)        # create table if not exists
    
    Session = sessionmaker(bind=engine)
    session = Session()

    products = [
        Product(
            name="에비앙",
            stock=10,
            price=1500,
            company_name="Evian",
            kcal=0,
            caffeine=0,
            carbon_acid=False,
            sugar=0,
            text_info="프랑스에서 온 고급 탄산수",
            image_path="assets/evian.webp"
        ),
        Product(
            name="핫식스",
            stock=10,
            price=1500,
            company_name="Hot6",
            kcal=100,
            caffeine=200,
            carbon_acid=True,
            sugar=50,
            text_info="잠깰 때 좋아요",
            image_path="assets/hot6.jpg"
        ),
    ]

    session.add_all(products)
    session.commit()

if __name__ == "__main__":
    main()