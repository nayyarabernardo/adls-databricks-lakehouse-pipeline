from src.silver.tables.customers import build_customers_silver
from src.silver.tables.brands import build_brands_silver
from src.silver.tables.products import build_products_silver
from src.silver.tables.orders import build_orders_silver 
from src.silver.tables.staffs import build_staffs_silver
from src.silver.tables.stocks import build_stocks_silver
from src.silver.tables.stores import build_stores_silver
from src.silver.tables.order_items import build_order_items_silver
from src.silver.tables.categories import build_categories_silver

# futuramente:
# from src.silver.orders import build_orders_silver

SILVER_TABLES = {
    "customers": {
        "builder": build_customers_silver,
        "bronze_suffix": "customers",
        "silver_suffix": "customers",
        "silver_table": "bikestore.logistics.silver_customers",
    }, 

    "brands": {
        "builder": build_brands_silver,
        "bronze_suffix": "brands",
        "silver_suffix": "brands",
        "silver_table": "bikestore.logistics.silver_brands",
    },
    "products": {
        "builder": build_products_silver,
        "bronze_suffix": "products",
        "silver_suffix": "products",
        "silver_table": "bikestore.logistics.silver_products",
    },
    "orders": {
        "builder": build_orders_silver,
        "bronze_suffix": "orders",
        "silver_suffix": "orders",
        "silver_table": "bikestore.logistics.silver_orders",
    },
    "staffs": {
        "builder": build_staffs_silver,
        "bronze_suffix": "staffs",
        "silver_suffix": "staffs",
        "silver_table": "bikestore.logistics.silver_staffs",
    },
    "categories": {
        "builder": build_categories_silver,
        "bronze_suffix": "categories",
        "silver_suffix": "categories",
        "silver_table": "bikestore.logistics.silver_categories",
    },
    "stocks": {
        "builder": build_stocks_silver,
        "bronze_suffix": "stocks",
        "silver_suffix": "stocks",
        "silver_table": "bikestore.logistics.silver_stocks",
    },
    "stores": {
        "builder": build_stores_silver,
        "bronze_suffix": "stores",
        "silver_suffix": "stores",
        "silver_table": "bikestore.logistics.silver_stores",
    },
    "order_items": {
        "builder": build_order_items_silver,
        "bronze_suffix": "order_items",
        "silver_suffix": "order_items",
        "silver_table": "bikestore.logistics.silver_order_items",
    },
}
