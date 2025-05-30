import sqlite3

conn = sqlite3.connect("vending_machine.db")
cur = conn.cursor()

# 테이블 생성
cur.execute(
    """
CREATE TABLE IF NOT EXISTS Product (
    id INTEGER PRIMARY KEY AUTOINCREMENT,      -- 상품ID
    name VARCHAR(20) NOT NULL,                 -- 상품명
    stock INT NOT NULL,                        -- 재고
    price INT NOT NULL,                        -- 가격
    company_name VARCHAR(20) NOT NULL,         -- 회사명
    kcal INT NOT NULL,                         -- 칼로리
    caffeine INT,                              -- 카페인 (NULL 허용)
    carbon_acid BOOLEAN,                       -- 탄산 (NULL 허용)
    sugar INT,                                 -- 당 (NULL 허용)
    text_info VARCHAR(200),                    -- 텍스트 (NULL 허용)
    image_path VARCHAR(100) NOT NULL           -- 이미지 경로
)
"""
)

cur.execute(
    """
CREATE TABLE IF NOT EXISTS "Order" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,      -- 주문ID
    product_id INT NOT NULL,                   -- 상품ID (외래키)
    order_at TIMESTAMP NOT NULL,               -- 주문시점
    payment_type CHAR(2) NOT NULL,             -- 결제타입
    cash_amount INT,                           -- 현금 (NULL 허용)
    card_info VARCHAR(50),                     -- 카드 (NULL 허용)
    cash_change INT,                           -- 거스름돈 (NULL 허용)
    FOREIGN KEY (product_id) REFERENCES Product(id)
)
"""
)

cur.execute(
    """
CREATE TABLE IF NOT EXISTS Receipt (
    id INTEGER PRIMARY KEY AUTOINCREMENT,      -- 영수증ID
    order_id INT NOT NULL,                     -- 주문ID (외래키)
    FOREIGN KEY (order_id) REFERENCES "Order"(id)
)
"""
)

# 데이터 삽입
cur.execute(
    """
    INSERT INTO Product
    (name, stock, price, company_name, kcal, caffeine, carbon_acid, sugar, text_info, image_path)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
    (
        "에비앙",
        10,
        1500,
        "Evian",
        0,
        0,
        0,
        0,
        "프랑스에서 온 고급 탄산수",
        "assets/evian.webp",
    ),
    (
        "핫식스",
        10,
        1500,
        "Hot6",
        100,
        200,
        True,
        50,
        "잠깰 때 좋아요",
        "assets/hot6.jpg",
    ),
)

# 데이터 조회
cur.execute("SELECT * FROM Product")
rows = cur.fetchall()
for row in rows:
    print(row)

conn.commit()
conn.close()
