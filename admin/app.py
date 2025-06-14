from flask import Flask, render_template, request
from . import controller

app = Flask(__name__)


@app.route("/")
def admin():
    return render_template("home.html", active_page="home")


@app.route("/inventory")
def inventory():
    product_list = controller.get_all_products()
    return render_template(
        "inventory.html", products=product_list, active_page="inventory"
    )


@app.route("/orders")
def orders():
    order_list = controller.get_all_orders()
    return render_template("orders.html", orders=order_list, active_page="orders")


@app.route("/update", methods=["POST"])
def update_product():
    form_data = dict(request.form)
    file = request.files.get("image_file")
    return controller.update_product(form_data, file)


if __name__ == "__main__":
    app.run(debug=True)
