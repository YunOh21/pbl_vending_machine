from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return "<h2>자판기 메인 페이지입니다</h2>"

@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/admin/inventory")
def inventory():
    return render_template("inventory.html")

@app.route("/admin/orders")
def orders():
    return render_template("orders.html")

@app.route("/admin/edit")
def edit():
    return render_template("edit.html")

if __name__ == "__main__":
    app.run(debug=True)