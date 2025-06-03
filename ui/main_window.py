from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
import sys

from core import controller


class VendingMachine(QWidget):
    def __init__(self):
        super().__init__()

        is_receipt = None
        is_change = None
        is_card = None
        is_drink_out = None
        is_cash = "Y"

        uic.loadUi("ui/vending_machine.ui", self)
        self.setWindowTitle("자판기")

        product_list = controller.get_all()
        
        products = QGridLayout(self.products)
        for i in range(3):
            for j in range(4):
                vbox = QVBoxLayout()
                img_label = QLabel()
                img_label.setPixmap(QPixmap("no_image.png"))
                img_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                img_label.setScaledContents(True)
                img_label.setStyleSheet(
                    "background-color: #eee; border: 1px solid #ccc;"
                )
                try:
                    btn = QPushButton(product_list[i * 4 + j].name)
                except:
                    btn = QPushButton(f"상품 {i * 4 + j + 1}")
                btn.setDisabled(True)
                vbox.addWidget(img_label)
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

        cash = QGridLayout(self.cash_box)
        for text in ["1000", "5000", "10000"]:
            btn = QPushButton(text)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            cash.addWidget(btn)

        # 상품 버튼 활성화
        if is_card or is_cash:
            for btn in self.products.findChildren(QPushButton):
                btn.setEnabled(True)

        # 영수증 버튼
        if is_receipt is None:
            self.receipt_box.hide()
            self.receipt_btn.hide()
        elif is_receipt == "asking":
            self.receipt_btn.setText("받기")
            self.receipt_btn.show()
            self.receipt_box.show()
        elif is_receipt == "printed":
            self.receipt_btn.setText("확인")
            self.receipt_btn.show()
            self.receipt_box.show()
        elif is_receipt == "collected":
            self.receipt_box.hide()
            self.receipt_btn.hide()

        # 카드 버튼
        if is_card is None:
            self.card_btn.setText("카드를\n넣으세요")
            self.card_btn.setStyleSheet("")
            self.card_btn.setDisabled(False)
        else:
            if is_receipt == "collected":
                self.card_btn.setText("카드\n찾아가세요")
                self.card_btn.setStyleSheet("color: red;")
                self.card_btn.setDisabled(False)
            else:
                self.card_btn.setText("카드가\n있어요")
                self.card_btn.setStyleSheet("")
                self.card_btn.setDisabled(True)

        # 거스름돈 버튼
        if is_change is None:
            self.change_box.hide()
            self.change_btn.hide()
        else:
            self.change_btn.setText("확인")
            self.change_btn.show()
            self.change_box.show()

        # 음료 받는 곳
        if is_drink_out is None:
            self.drink_btn.hide()
        else:
            self.drink_btn.show()

        self.school_label.setPixmap(QPixmap("assets/erica_pbl.png"))
        self.school_label.setScaledContents(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet("QWidget { font-size: 12pt; }")
    window = VendingMachine()
    window.show()
    sys.exit(app.exec_())
