from flask import Flask, render_template
from . import controller

app = Flask(__name__)


@app.route("/")
def admin():
    return render_template("admin.html")


@app.route("/admin/inventory")
def inventory():
    return render_template("inventory.html")


@app.route("/admin/orders")
def orders():
    order_list = controller.get_all_orders()
    return render_template("orders.html", orders=order_list)


@app.route("/admin/edit")
def edit():
    return render_template("edit.html")


@app.route("/admin/test")
def test():
    return render_template("test.html")


if __name__ == "__main__":
    app.run(debug=True)
