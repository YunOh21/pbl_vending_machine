import os
from werkzeug.utils import secure_filename
from db import db_admin
from common.dto import *


def get_all_products():
    return db_admin.get_all_products()


def get_all_orders():
    return db_admin.get_all_orders()


def update_product(form_data, file):
    try:
        if file and hasattr(file, "filename") and file.filename:
            filename = secure_filename(file.filename)
            save_dir = os.path.join("assets")
            os.makedirs(save_dir, exist_ok=True)
            save_path = os.path.join(save_dir, filename)
            file.save(save_path)

        # 입력값 검증 및 변환
        product_id = form_data.get("product_id")
        if not product_id:
            raise ValueError("product_id is required")

        product_name = form_data.get("product_name")
        if not product_name:
            raise ValueError("product_name is required")

        stock = form_data.get("stock")
        if stock is None or stock == "":
            raise ValueError("stock is required")
        stock = int(stock)

        price = form_data.get("price")
        if price is None or price == "":
            raise ValueError("price is required")
        price = int(price)

        company_name = form_data.get("company_name")
        if not company_name:
            raise ValueError("company_name is required")

        kcal = form_data.get("kcal")
        kcal = int(kcal) if kcal and kcal.isdigit() else None

        caffeine = form_data.get("caffeine")
        caffeine = int(caffeine) if caffeine and caffeine.isdigit() else None

        carbon_acid = form_data.get("carbon_acid")
        carbon_acid = (
            int(carbon_acid) if carbon_acid and carbon_acid.isdigit() else None
        )

        sugar = form_data.get("sugar")
        sugar = int(sugar) if sugar and sugar.isdigit() else None

        product = ProductData(
            product_id=product_id,
            product_name=product_name,
            stock=stock,
            price=price,
            company_name=company_name,
            kcal=kcal,
            caffeine=caffeine,
            carbon_acid=carbon_acid,
            sugar=sugar,
            image_path=filename,
        )

        # 실제 DB 업데이트 호출
        db_admin.update_product(product)

        return {"result": "ok", "product": product.__dict__}

    except ValueError as ve:
        return {"result": "error", "message": str(ve)}
    except Exception as e:
        return {"result": "error", "message": "Unexpected error occurred: " + str(e)}
