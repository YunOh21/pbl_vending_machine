from flask import Flask, render_template, request, send_from_directory
from . import admin_controller
import os

app = Flask(__name__)

# assets 폴더의 절대 경로 구하기
ASSETS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets"))


@app.route("/<path:filename>")
def assets(filename):
    return send_from_directory(ASSETS_DIR, filename)


@app.route("/")
def admin():
    return render_template("home.html", active_page="home")


@app.route("/inventory")
def inventory():
    product_list = admin_controller.get_all_products()
    return render_template(
        "inventory.html", products=product_list, active_page="inventory"
    )


@app.route("/orders")
def orders():
    order_list = admin_controller.get_all_orders()
    return render_template("orders.html", orders=order_list, active_page="orders")


@app.route("/update", methods=["POST"])
def update_product():
    form_data = dict(request.form)
    file = request.files.get("image_file")
    return admin_controller.update_product(form_data, file)


if __name__ == "__main__":
    app.run(debug=True)
