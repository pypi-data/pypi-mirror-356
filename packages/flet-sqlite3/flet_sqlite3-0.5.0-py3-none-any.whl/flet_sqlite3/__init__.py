"""
flet_sqlite3 - Приложение для учета партнеров и расчета скидок с использованием Flet и SQLite3
"""

__version__ = "0.5.0"

# Импортируем основные модули для удобства использования
from . import database
from . import main

# Экспортируем основные функции
from .database import (
    get_partners,
    get_partners_with_discounts,
    calculate_partner_discount,
    get_partner_total_sales,
    add_partner,
    update_partner,
    delete_partner
)

# Экспортируем функцию запуска приложения
def start_app():
    """Запуск приложения"""
    import flet as ft
    from .main import main
    ft.app(target=main) 