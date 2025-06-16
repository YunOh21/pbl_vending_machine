from .dao import *

from common.logger import LoggerManager

logger = LoggerManager().get_logger()


def main():
    engine = create_engine("sqlite:///db/vending_machine.db")
    Base.metadata.create_all(engine)  # create table if not exists

    Session = sessionmaker(bind=engine)
    session = Session()

    products = [
        Product(
            name="에비앙(탄산)",
            stock=10,
            price=1500,
            company_name="Evian",
            kcal=0,
            caffeine=0,
            carbon_acid=False,
            sugar=0,
            text_info="프랑스에서 온 고급 탄산수",
            image_path="evian.webp",
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
            image_path="hot6.jpg",
        ),
        Product(
            name="바리스타",
            stock=10,
            price=1800,
            company_name="Maeil",
            kcal=120,
            caffeine=60,
            carbon_acid=False,
            sugar=15,
            text_info="진한 커피의 맛",
            image_path="barista.jpg",
        ),
        Product(
            name="레쓰비",
            stock=10,
            price=1200,
            company_name="롯데칠성",
            kcal=100,
            caffeine=50,
            carbon_acid=False,
            sugar=18,
            text_info="달콤한 커피음료",
            image_path="letsbe.jpg",
        ),
        Product(
            name="포카리",
            stock=10,
            price=1600,
            company_name="Otsuka",
            kcal=50,
            caffeine=0,
            carbon_acid=False,
            sugar=12,
            text_info="이온음료의 대표주자",
            image_path="pocari.png",
        ),
        Product(
            name="데자와",
            stock=10,
            price=1700,
            company_name="동서식품",
            kcal=80,
            caffeine=30,
            carbon_acid=False,
            sugar=20,
            text_info="홍차의 풍미",
            image_path="tejava.png",
        ),
        Product(
            name="카페라테",
            stock=10,
            price=2000,
            company_name="매일유업",
            kcal=90,
            caffeine=100,
            carbon_acid=False,
            sugar=21,
            text_info="커피와 우유",
            image_path="latte.jpg",
        ),
        Product(
            name="몬스터",
            stock=10,
            price=1300,
            company_name="몬스터 베버리지",
            kcal=150,
            caffeine=500,
            carbon_acid=True,
            sugar=35,
            text_info="시험기간에 함께해요",
            image_path="monster.webp",
        ),
        Product(
            name="삼다수",
            stock=10,
            price=900,
            company_name="제주삼다수",
            kcal=0,
            caffeine=0,
            carbon_acid=False,
            sugar=0,
            text_info="제주에서 왔어요",
            image_path="samda.png",
        ),
        Product(
            name="솔의눈",
            stock=10,
            price=1300,
            company_name="롯데칠성",
            kcal=10,
            caffeine=0,
            carbon_acid=False,
            sugar=2,
            text_info="누가 이거 먹자고 했냐",
            image_path="sol.jpg",
        ),
        Product(
            name="베지밀비",
            stock=10,
            price=1500,
            company_name="정식품",
            kcal=150,
            caffeine=0,
            carbon_acid=False,
            sugar=3,
            text_info="건강한 비건 음료",
            image_path="soy.jpg",
        ),
        Product(
            name="이프로",
            stock=10,
            price=1200,
            company_name="롯데칠성",
            kcal=20,
            caffeine=0,
            carbon_acid=False,
            sugar=2,
            text_info="2% 부족할 때",
            image_path="2pro.jpg",
        ),
    ]

    session.add_all(products)
    session.commit()


if __name__ == "__main__":
    main()
    logger.info("DB successfully started")
