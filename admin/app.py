from flask import Flask, render_template
from . import controller

app = Flask(__name__)


@app.route("/")
def admin():
    return render_template("home.html", active_page="home")


@app.route("/admin/inventory")
def inventory():
    product_list = controller.get_all_products()
    return render_template(
        "inventory.html", products=product_list, active_page="inventory"
    )


@app.route("/admin/orders")
def orders():
    order_list = controller.get_all_orders()
    return render_template("orders.html", orders=order_list, active_page="orders")


if __name__ == "__main__":
    app.run(debug=True)
