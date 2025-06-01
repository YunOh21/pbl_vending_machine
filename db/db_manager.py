import sqlite3


def get_all():
    conn = sqlite3.connect("vending_machine.db")
    cur = conn.cursor()

    product_list = []

    cur.execute("SELECT * FROM Product")
    rows = cur.fetchall()
    for row in rows:
        product_list.append(row)

    conn.commit()
    conn.close()

    return product_list
