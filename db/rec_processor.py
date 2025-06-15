from sqlalchemy.orm import Query
from sqlalchemy import func
from .dao import *


def rec_caffeine(query: Query):
    return (
        query.join(Order, Product.id == Order.product_id)
        .filter(Product.stock > 0)
        .group_by(Product.id)
        .order_by(Product.caffeine.desc(), func.count(Order.product_id).desc())
    )


def rec_kcal(query: Query):
    return (
        query.join(Order, Product.id == Order.product_id)
        .filter(Product.stock > 0)
        .group_by(Product.id)
        .order_by(Product.kcal.asc(), func.count(Order.product_id).desc())
    )


def rec_carbon_acid(query: Query):
    return (
        query.join(Order, Product.id == Order.product_id)
        .filter(Product.stock > 0)
        .group_by(Product.id)
        .order_by(Product.carbon_acid.desc(), func.count(Order.product_id).desc())
    )


def rec_no_caffeine(query: Query):
    return (
        query.join(Order, Product.id == Order.product_id)
        .filter(Product.stock > 0, Product.caffeine == 0)
        .group_by(Product.id)
        .order_by(func.count(Order.product_id).desc())
    )


def rec_any(query: Query):
    return (
        query.join(Order, Product.id == Order.product_id)
        .filter(Product.stock > 0)
        .group_by(Product.id)
        .order_by(func.count(Order.product_id).desc())
    )


RECOMMEND_STRATEGIES = {
    "caffeine": rec_caffeine,
    "kcal": rec_kcal,
    "carbon_acid": rec_carbon_acid,
    "no_caffeine": rec_no_caffeine,
    "any": rec_any,
}


def get_rec_query_by_type(rec_type: str, query: Query):
    strategy = RECOMMEND_STRATEGIES.get(rec_type)
    if not strategy:
        raise ValueError("알 수 없는 추천 타입입니다.")
    return strategy(query)
