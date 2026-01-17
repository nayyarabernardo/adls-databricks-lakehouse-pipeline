from src.gold.tables.sales_ny import build_sales_ny_gold
from src.gold.tables.orders_pending import build_orders_pending_gold


GOLD_TABLES = {
    "sales_ny": {
        "gold_table": "bikestore.logistics.sales_ny",
        "gold_suffix": "sales_ny",
        "builder": build_sales_ny_gold
    },
    "orders_pending": {
        "gold_table": "bikestore.logistics.orders_pending",
        "gold_suffix": "orders_pending",
        "builder": build_orders_pending_gold
    }
}

