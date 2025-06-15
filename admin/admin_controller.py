import os
from werkzeug.utils import secure_filename
from db import db_admin
from common.dto import *
import logging


logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("admin_controller")


def get_all_products():
    logger.debug("get_all_products")
    return db_admin.get_all_products()


def get_all_orders():
    logger.debug("get_all_orders")
    return db_admin.get_all_orders()


def update_product(form_data, file):
    logger.debug("update_product")
    try:
        if file and hasattr(file, "filename") and file.filename:
            filename = secure_filename(file.filename)
            save_dir = os.path.join("assets")
            os.makedirs(save_dir, exist_ok=True)
            save_path = os.path.join(save_dir, filename)
            file.save(save_path)
        else:
            filename = form_data.get("old_image_path")

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

        carbon_acid_str = form_data.get("carbon_acid")
        logger.debug(f"carbon_acid_str: {carbon_acid_str}")

        carbon_acid = True if carbon_acid_str == "1" else False

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

        return db_admin.update_product(product)

    except ValueError as ve:
        logger.error("update_product ValueError {ve}")
        return {"result": "error", "message": str(ve)}
    except Exception as e:
        logger.error("update_product Exception {e}")
        return {"result": "error", "message": "Unexpected error occurred: " + str(e)}


def shutdown():
    logger.debug("shutdown")
    return db_admin.update_all_zero()
