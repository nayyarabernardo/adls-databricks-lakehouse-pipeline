from src.silver.tables.silver_customers import build_customers_silver
from src.silver.tables.silver_products import build_products_silver
from src.silver.tables.silver_orders import build_orders_silver 


SILVER_TABLES = {
    "customers": {
        "builder": build_customers_silver,
        "bronze_suffix": "customers",
        "silver_suffix": "customers",
        "silver_table": "bikestore.logistics.silver_customers",
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
    }
 }
