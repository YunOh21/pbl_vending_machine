from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
import sys, os

from core import controller


class VendingMachine(QWidget):
    def __init__(self):
        super().__init__()

        uic.loadUi("ui/vending_machine.ui", self)
        self.setWindowTitle("자판기")

        self.show_product_list()
        self.create_all()
        self.set_init_status()

    def show_product_list(self):
        self.product_list = controller.get_all_products()

        products = QGridLayout(self.products)
        for i in range(3):
            for j in range(4):
                vbox = QVBoxLayout()
                img_label = QLabel()
                img_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                img_label.setScaledContents(True)
                img_label.setStyleSheet(
                    "background-color: #eee; border: 1px solid #ccc;"
                )
                price_label = QLabel()
                price_label.setAlignment(Qt.AlignCenter)
                stock_label = QLabel()
                stock_label.setAlignment(Qt.AlignRight)
                try:
                    product = self.product_list[i * 4 + j]
                    name = product.name
                    id = product.id
                    price = product.price
                    img_path = product.image_path

                    btn = QPushButton(name)
                    btn.setProperty("id", id)
                    btn.setProperty("price", price)

                    if not os.path.exists(img_path):
                        img_path = "assets/no_image.gif"
                    img_label.setPixmap(QPixmap(img_path))
                    price_label.setText(f"₩{price:,}")
                except:
                    btn = QPushButton(f"상품 {i * 4 + j + 1}")
                btn.setDisabled(True)
                vbox.addWidget(img_label)
                vbox.addWidget(price_label)
                vbox.addWidget(btn)

                container = QWidget()
                container.setLayout(vbox)
                products.addWidget(container, i, j)

        recommend = QGridLayout(self.recommend)
        for text in ["졸려요", "다이어트", "탄산", "무카페인", "아무거나"]:
            btn = QPushButton(text)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            btn.setDisabled(True)
            recommend.addWidget(btn)

    def create_all(self):
        cash = QGridLayout(self.cash_box)
        for text in ["1000", "5000", "10000"]:
            btn = QPushButton(text)
            btn.setProperty("amount", int(text))
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            cash.addWidget(btn)

        drink_box = QVBoxLayout(self.drink_box)
        self.receive_drink_img = QLabel()
        self.receive_drink_img.setFixedSize(100, 100)
        self.receive_drink_btn = QPushButton("받았습니다!")
        self.receive_drink_btn.setFixedWidth(100)
        drink_box.addWidget(self.receive_drink_img, alignment=Qt.AlignHCenter)
        drink_box.addWidget(self.receive_drink_btn, alignment=Qt.AlignHCenter)

        self.card_btn.clicked.connect(self.set_card_status)

        for btn in self.cash_box.findChildren(QPushButton):
            btn.clicked.connect(self.set_cash_status)
        self.return_cash_btn.clicked.connect(self.return_cash)

        for btn in self.products.findChildren(QPushButton):
            btn.clicked.connect(self.place_order)

        self.receive_drink_btn.clicked.connect(self.on_drink_received)
        self.change_btn.clicked.connect(self.on_change_received)

        # 학교 로고
        self.school_label.setPixmap(QPixmap("assets/erica_pbl.png"))
        self.school_label.setScaledContents(True)

        # goodbye
        self.goodbye_layout = QGridLayout(self.goodbye)

        self.goodbye_bubble = QLabel()
        self.goodbye_bubble.setPixmap(QPixmap("assets/bubble2.png"))
        self.goodbye_bubble.setScaledContents(True)
        self.goodbye_bubble.setAlignment(Qt.AlignCenter)

        self.goodbye_text = QLabel()
        self.goodbye_text.setStyleSheet(
            """
            color: #333;
            font-size: 11pt;
            font-weight: bold;
            background: transparent;
        """
        )

        self.goodbye_text.setMargin(15)
        self.goodbye_text.setAlignment(Qt.AlignCenter)

        self.goodbye_layout.addWidget(self.goodbye_bubble, 0, 0)
        self.goodbye_layout.addWidget(self.goodbye_text, 0, 0)

        self.goodbye_bubble.hide()
        self.goodbye_text.hide()

    def on_change_received(self):
        self.goodbye_text.setText(
            f"{self.cash_amount:,}원을 돌려드렸습니다. 안녕히 가세요."
        )
        self.goodbye_bubble.show()
        self.goodbye_text.show()

        self.change_box.hide()
        self.cash_amount = 0
        self.is_processing = False
        self.order_id = None

        QTimer.singleShot(
            5000,
            lambda: (
                self.goodbye_bubble.hide(),
                self.goodbye_text.hide(),
                self.set_init_status(),
            ),
        )

    def on_drink_received(self):
        self.receive_drink_img.hide()
        self.receive_drink_btn.hide()
        self.cash_label.hide()
        self.cash_display.hide()
        self.return_cash_btn.hide()
        self.change_box.show()
        self.change_btn.setText(f"₩{self.cash_amount:,} 받기")
        self.change_btn.show()

    def place_order(self):
        btn = self.sender()
        product_id = btn.property("id")
        self.order_id = controller.place_order(product_id, self.payment_type)
        if self.order_id:
            self.cash_amount -= btn.property("price")
            self.set_cash_btn()
            self.give_drink()

    def return_cash(self):
        self.cash_amount = 0
        self.is_processing = False
        self.set_card_btn()
        self.set_cash_btn()
        self.set_order_btn()

    def set_cash_status(self):
        btn = self.sender()
        self.cash_amount += btn.property("amount")
        self.is_processing = True
        self.set_cash_btn()
        self.set_card_btn()
        self.set_order_btn()

    def set_card_status(self):
        if self.is_card:
            self.is_card = False
            self.payment_type = "CASH"
        else:
            self.is_card = True
            self.payment_type = "CARD"
        self.set_card_btn()
        self.set_cash_btn()
        self.set_order_btn()

    def set_init_status(self):
        self.is_receipt = False
        self.is_change = False
        self.is_card = False
        self.is_cash = False
        self.is_processing = False

        self.payment_type = "CASH"
        self.cash_amount = 0
        self.order_id = None

        self.set_order_btn()
        self.set_receipt_btn()
        self.set_card_btn()
        self.set_cash_btn()
        self.set_change_btn()
        self.set_receive_drink_btn()

    def set_card_btn(self):
        if self.is_card:
            if self.is_receipt == "collected":
                self.card_btn.setText("카드\n찾아가세요")
                self.card_btn.setStyleSheet("color: red;")
                self.card_btn.setDisabled(False)
            else:
                self.card_btn.setText("카드가\n있어요")
                self.card_btn.setStyleSheet("")
                self.card_btn.setDisabled(False)
        else:
            self.card_btn.setText("카드를\n넣으세요")
            self.card_btn.setStyleSheet("")
            self.card_btn.setDisabled(False)

        if self.is_processing:
            self.card_btn.setText("결제중...")
            self.card_btn.setDisabled(True)

    def set_cash_btn(self):
        if self.is_card:
            for btn in self.cash_box.findChildren(QPushButton):
                btn.setEnabled(False)
        else:
            if self.cash_amount != 0:
                self.cash_label.show()
                self.cash_display.setText(f"₩{self.cash_amount:,}")
                self.cash_display.show()
                self.return_cash_btn.show()
            else:
                self.return_cash_btn.hide()
                self.cash_display.setText("")
                self.cash_display.hide()
                self.cash_label.hide()
            for btn in self.cash_box.findChildren(QPushButton):
                btn.setEnabled(True)

        if self.order_id:
            self.return_cash_btn.setEnabled(False)
            for btn in self.cash_box.findChildren(QPushButton):
                btn.setEnabled(False)

    def set_order_btn(self):
        if self.is_card or self.cash_amount != 0:
            self.help_label.hide()
            for btn in self.products.findChildren(QPushButton):
                if (self.is_card) or (btn.property("price") <= self.cash_amount):
                    btn.setEnabled(True)
                elif btn.property("price") > self.cash_amount:
                    btn.setEnabled(False)
            if (self.is_card) or self.cash_amount >= 2000:
                for btn in self.recommend.findChildren(QPushButton):
                    btn.setEnabled(True)
        else:
            self.help_label.show()
            for btn in self.products.findChildren(QPushButton):
                btn.setEnabled(False)
            for btn in self.recommend.findChildren(QPushButton):
                btn.setEnabled(False)

    def set_receipt_btn(self):
        if not self.is_receipt:
            self.receipt_box.hide()
            self.receipt_btn.hide()
        elif self.order_id:
            self.receipt_btn.setText("받기")
            self.receipt_btn.show()
            self.receipt_box.show()
        elif self.is_receipt == "printed":
            self.receipt_btn.setText("확인")
            self.receipt_btn.show()
            self.receipt_box.show()
        elif self.is_receipt == "collected":
            self.receipt_box.hide()
            self.receipt_btn.hide()

    def set_change_btn(self):
        if self.is_change:
            self.change_btn.setText("확인")
            self.change_btn.show()
            self.change_box.show()
        else:
            self.change_box.hide()
            self.change_btn.hide()

    def set_receive_drink_btn(self):
        self.receive_drink_img.hide()
        self.receive_drink_btn.hide()

    def give_drink(self):
        if self.order_id:
            product_id = controller.get_ordered_product(self.order_id)
            product = controller.get_one_product(product_id)
            img_path = product.image_path
            if not os.path.exists(img_path):
                img_path = "assets/no_image.gif"

            pixmap = QPixmap(img_path)
            if not pixmap.isNull():
                # 세로 크기만 라벨에 맞춤, 가로는 자동(비율 유지)
                scaled_pixmap = pixmap.scaledToHeight(
                    self.receive_drink_img.height(), Qt.SmoothTransformation
                )
                self.receive_drink_img.setPixmap(scaled_pixmap)
            self.receive_drink_img.show()

            # "받았습니다" 버튼 표시
            self.receive_drink_btn.show()
        else:
            self.receive_drink_img.hide()
            self.receive_drink_btn.hide()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet("QWidget { font-size: 12pt; }")
    window = VendingMachine()
    window.show()

    sys.exit(app.exec_())
