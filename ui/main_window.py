from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
import sys, os, logging

from core import core_controller
from common.dto import *

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

logger = logging.getLogger("main_window")


class VendingMachine(QWidget):
    def __init__(self):
        super().__init__()

        uic.loadUi("ui/vending_machine.ui", self)
        self.setWindowTitle("자판기")

        self.show_product_list(True)
        self.create_all()
        self.set_init_status()

    def show_product_list(self, is_starting):
        if not is_starting:
            # 1. 기존 레이아웃과 위젯 완전 제거
            old_layout = self.products.layout()
            if old_layout is not None:
                while old_layout.count():
                    item = old_layout.takeAt(0)
                    widget = item.widget()
                    if widget is not None:
                        widget.setParent(None)
                        widget.deleteLater()
                # 레이아웃 자체도 삭제
                QWidget().setLayout(old_layout)  # 기존 레이아웃을 orphan 시킴

        self.product_list = core_controller.get_all_products()
        self.is_soldout = all(product.stock == 0 for product in self.product_list)

        # 2. 새 레이아웃 할당
        products = QGridLayout()
        self.products.setLayout(products)

        for i in range(3):
            for j in range(4):
                vbox = QVBoxLayout()

                img_label = QLabel()
                img_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                img_label.setScaledContents(True)
                img_label.setStyleSheet(
                    "background-color: #eee; border: 1px solid #ccc;"
                )

                stock_label = QLabel(img_label)
                stock_label.setAlignment(Qt.AlignBottom | Qt.AlignRight)
                stock_label.setStyleSheet(
                    "color: blue; padding: 1px; font-size: 10px; background: transparent;"
                )
                stock_label.setAttribute(Qt.WA_TransparentForMouseEvents)

                price_label = QLabel()
                price_label.setAlignment(Qt.AlignCenter)

                try:
                    product = self.product_list[i * 4 + j]
                    name = product.name
                    id = product.id
                    price = product.price
                    stock = product.stock
                    img_path = product.image_path

                    btn = QPushButton(name)
                    btn.setProperty("id", id)
                    btn.setProperty("price", price)
                    btn.setProperty("stock", stock)
                    btn.clicked.connect(self.place_order_by_id)

                    assets_img_path = "assets/" + img_path

                    if not os.path.exists(assets_img_path):
                        assets_img_path = "assets/no_image.gif"
                    img_label.setPixmap(QPixmap(assets_img_path))
                    price_label.setText(f"₩{price:,}")
                    stock_label.setText(f"재고: {stock}")

                    if stock == 0:
                        stock_label.setStyleSheet(
                            "color: gray; padding: 1px; font-size: 10px; background: transparent;"
                        )
                except:
                    btn = QPushButton(f"상품 {i * 4 + j + 1}")
                    stock_label.setText("")
                btn.setDisabled(True)

                vbox.addWidget(img_label)
                vbox.addWidget(price_label)
                vbox.addWidget(btn)

                container = QWidget()
                container.setLayout(vbox)
                products.addWidget(container, i, j)

    def create_all(self):
        recommend = QGridLayout(self.recommend)
        button_info = [
            ("졸려요", "caffeine"),
            ("다이어트", "kcal"),
            ("탄산", "carbon_acid"),
            ("무카페인", "no_caffeine"),
            ("아무거나", "any"),
        ]
        for text, type in button_info:
            btn = QPushButton(text)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            btn.setProperty("type", type)
            btn.clicked.connect(self.place_order_by_rec)
            recommend.addWidget(btn)

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
        self.is_payment_processing = False
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

        if self.payment_type == "CASH":
            self.cash_label.hide()
            self.cash_display.hide()
            self.return_cash_btn.hide()
            self.change_box.show()
            self.change_btn.setText(f"₩{self.cash_amount:,} 받기")
            self.change_btn.show()
        else:
            self.is_payment_processing = False
            # 카드 결제 시 영수증 수령 여부 팝업
            reply = QMessageBox.question(
                self,
                "영수증 발급",
                "영수증을 받으시겠습니까?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.Yes,
            )
            if reply == QMessageBox.Yes:
                core_controller.add_receipt(self.order_id)
                QMessageBox.information(
                    self,
                    "영수증",
                    "영수증이 발급되었습니다.\n카드와 영수증을 가져가세요.",
                )
                self.is_receipt = "printed"
            else:
                QMessageBox.information(self, "감사합니다.", "카드를 가져가세요.")
                self.is_receipt = "collected"

            self.set_card_btn()

    def process_order(self, product_id, product_price):
        self.is_order_processing = True
        self.set_order_btn()

        change = None
        if self.payment_type == "CASH":
            change = self.cash_amount - product_price

        order_dto = OrderData(
            product_id=product_id,
            payment_type=self.payment_type,
            input_cash_amount=self.cash_amount,
            card_info=self.card_info,
            change=change,
        )

        self.order_id = core_controller.place_order(order_dto)
        if self.order_id and self.payment_type == "CASH":
            self.cash_amount -= product_price
            self.set_cash_btn()
        else:
            self.is_payment_processing = True
            self.set_card_btn()
        self.give_drink()

    def place_order_by_id(self):
        btn = self.sender()
        product_id = btn.property("id")
        product_price = btn.property("price")
        self.process_order(product_id, product_price)

    def place_order_by_rec(self):
        btn = self.sender()
        rec_type = btn.property("type")
        rec_product = core_controller.get_rec_product(rec_type)
        self.process_order(rec_product.id, rec_product.price)

    def return_cash(self):
        self.cash_amount = 0
        self.is_payment_processing = False
        self.set_card_btn()
        self.set_cash_btn()
        self.set_order_btn()

    def info_soldout(self):
        QMessageBox.information(
            self,
            "재고 소진",
            "주문할 수 있는 상품이 없습니다.\n결제수단을 가져가세요.",
        )

    def set_cash_status(self):
        if self.is_soldout:
            self.info_soldout()
        btn = self.sender()
        self.cash_amount += btn.property("amount")
        self.is_payment_processing = True
        self.set_cash_btn()
        self.set_card_btn()
        self.set_order_btn()

    def set_card_status(self):
        if self.is_soldout and self.payment_type == "CASH":
            self.info_soldout()

        if self.is_receipt:
            self.set_init_status()
        else:
            if self.payment_type == "CARD":
                self.payment_type = "CASH"
            else:
                self.payment_type = "CARD"
            self.set_card_btn()
            self.set_cash_btn()
            self.set_order_btn()

    def set_init_status(self):
        self.is_receipt = False
        self.is_change = False
        self.is_payment_processing = False
        self.is_order_processing = False

        self.payment_type = "CASH"
        self.cash_amount = 0
        self.order_id = None
        self.card_info = None

        self.set_order_btn()
        self.set_card_btn()
        self.set_cash_btn()
        self.set_change_btn()
        self.set_receive_drink_btn()

    def set_card_btn(self):
        self.card_btn.setDisabled(False)

        if self.payment_type == "CARD":
            if self.is_receipt == "collected":
                self.card_btn.setText("카드 꺼내기")
                self.card_btn.setStyleSheet("color: red;")
            elif self.is_receipt == "printed":
                self.card_btn.setText("카드와\n영수증\n받기")
                self.card_btn.setStyleSheet("color: red;")
            else:
                self.card_btn.setText("주문 안 하고\n카드 꺼내기")
                self.card_btn.setStyleSheet("")
        else:
            self.card_btn.setText("카드를\n넣으세요")
            self.card_btn.setStyleSheet("")

        if self.is_payment_processing:
            self.card_btn.setText("결제중...")
            self.card_btn.setDisabled(True)

    def set_cash_btn(self):
        if self.payment_type == "CARD":
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
        # 1. 주문 처리 중이면 모든 버튼 비활성화
        if self.is_order_processing:
            for btn in self.recommend.findChildren(QPushButton):
                btn.setEnabled(False)
            for btn in self.products.findChildren(QPushButton):
                btn.setEnabled(False)
            return  # 아래 로직 실행하지 않음

        # 2. 기존 로직
        if not self.is_soldout:
            if self.payment_type == "CARD":
                self.help_label.hide()
                for btn in self.recommend.findChildren(QPushButton):
                    btn.setEnabled(True)
                for btn in self.products.findChildren(QPushButton):
                    if btn.property("stock") > 0:
                        btn.setEnabled(True)
                    elif btn.property("price") > self.cash_amount:
                        btn.setEnabled(False)
            elif self.cash_amount != 0:
                self.help_label.hide()
                for btn in self.recommend.findChildren(QPushButton):
                    btn.setEnabled(True)
                for btn in self.products.findChildren(QPushButton):
                    if btn.property("price") <= self.cash_amount:
                        btn.setEnabled(True)
                    else:
                        btn.setEnabled(False)
            else:
                self.help_label.show()
                for btn in self.products.findChildren(QPushButton):
                    btn.setEnabled(False)
                for btn in self.recommend.findChildren(QPushButton):
                    btn.setEnabled(False)

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
            product_id = core_controller.get_ordered_product(self.order_id)
            product = core_controller.get_one_product(product_id)
            img_path = "assets/" + product.image_path
            if not os.path.exists(img_path):
                img_path = "assets/no_image.gif"

            pixmap = QPixmap(img_path)
            if not pixmap.isNull():
                img_label = QLabel()
                img_label.setFixedSize(100, 100)
                img_label.setAlignment(Qt.AlignCenter)

                scaled_pixmap = pixmap.scaled(
                    img_label.width(),
                    img_label.height(),
                    Qt.IgnoreAspectRatio,
                    Qt.SmoothTransformation,
                )
                self.receive_drink_img.setPixmap(scaled_pixmap)

            self.show_product_list(False)  # 재고 표시 수정
            self.receive_drink_img.show()

            # "받았습니다" 버튼 표시
            self.receive_drink_btn.show()
        else:
            QMessageBox.critical(
                self, "오류", "문제가 발생했습니다. 관리자에게 문의하세요."
            )
            self.receive_drink_img.hide()
            self.receive_drink_btn.hide()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet("QWidget { font-size: 12pt; }")
    window = VendingMachine()
    window.show()

    sys.exit(app.exec_())
