import unittest
import sqlite3
import os
import database as db
from datetime import datetime

class TestDatabaseFunctions(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # Создаем тестовую базу данных
        cls.test_db_path = 'test_database.db'
        # Сохраняем оригинальный путь к базе данных
        cls.original_path = db.path
        # Устанавливаем путь к тестовой базе данных
        db.path = cls.test_db_path
        # Инициализируем базу данных
        db.init_dp()
        # Добавляем тестовые данные
        cls._add_test_data()
    
    @classmethod
    def tearDownClass(cls):
        # Возвращаем оригинальный путь к базе данных
        db.path = cls.original_path
        # Удаляем тестовую базу данных
        if os.path.exists(cls.test_db_path):
            os.remove(cls.test_db_path)
    
    @classmethod
    def _add_test_data(cls):
        conn = sqlite3.connect(cls.test_db_path)
        cursor = conn.cursor()
        
        # Добавляем тестовые типы продуктов
        cursor.executemany(
            "INSERT INTO Product_type_import (type, kaof_type) VALUES (?, ?)",
            [('Тестовый тип 1', 1.5), ('Тестовый тип 2', 2.5)]
        )
        
        # Добавляем тестовых партнеров
        cursor.executemany(
            "INSERT INTO Partners_import (type, name, director, male, phone, adress, inn, rate) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            [
                ('ООО', 'Тестовый партнер 1', 'Иванов И.И.', 'test1@mail.ru', '123456789', 'Адрес 1', '1234567890', 5),
                ('ЗАО', 'Тестовый партнер 2', 'Петров П.П.', 'test2@mail.ru', '987654321', 'Адрес 2', '0987654321', 8)
            ]
        )
        
        # Добавляем тестовые продукты
        cursor.executemany(
            "INSERT INTO Products_import (type_id, Name, articul, min_price) VALUES (?, ?, ?, ?)",
            [(1, 'Тестовый продукт 1', 12345, 1000.0), (2, 'Тестовый продукт 2', 54321, 2000.0)]
        )
        
        # Добавляем тестовые продукты партнеров
        cursor.executemany(
            "INSERT INTO Partner_products_import (product_id, partner_id, Value, Data) VALUES (?, ?, ?, ?)",
            [
                (1, 1, 5000, datetime.now().isoformat()),
                (2, 1, 8000, datetime.now().isoformat()),
                (1, 2, 60000, datetime.now().isoformat()),
                (2, 2, 300000, datetime.now().isoformat())
            ]
        )
        
        conn.commit()
        conn.close()
    
    def test_get_partners(self):
        """Тест функции получения списка партнеров"""
        partners = db.get_partners()
        self.assertEqual(len(partners), 2)
        self.assertEqual(partners[0][2], 'Тестовый партнер 1')
        self.assertEqual(partners[1][2], 'Тестовый партнер 2')
    
    def test_calculate_partner_discount(self):
        """Тест функции расчета скидки для партнера"""
        # Партнер 1 имеет общий объем продаж 13000 (5000 + 8000) - скидка должна быть 5%
        discount1 = db.calculate_partner_discount(1)
        self.assertEqual(discount1, 5)
        
        # Партнер 2 имеет общий объем продаж 360000 (60000 + 300000) - скидка должна быть 15%
        discount2 = db.calculate_partner_discount(2)
        self.assertEqual(discount2, 15)
    
    def test_get_partner_total_sales(self):
        """Тест функции получения общего объема продаж партнера"""
        total_sales1 = db.get_partner_total_sales(1)
        self.assertEqual(total_sales1, 13000)
        
        total_sales2 = db.get_partner_total_sales(2)
        self.assertEqual(total_sales2, 360000)
    
    def test_get_partners_with_discounts(self):
        """Тест функции получения списка партнеров со скидками"""
        partners_with_discounts = db.get_partners_with_discounts()
        self.assertEqual(len(partners_with_discounts), 2)
        
        # Проверяем, что для каждого партнера добавлены поля скидки и общего объема продаж
        self.assertEqual(len(partners_with_discounts[0]), 11)  # 9 полей партнера + скидка + общий объем продаж
        self.assertEqual(partners_with_discounts[0][9], 5)     # Скидка первого партнера
        self.assertEqual(partners_with_discounts[0][10], 13000) # Общий объем продаж первого партнера
        
        self.assertEqual(partners_with_discounts[1][9], 15)    # Скидка второго партнера
        self.assertEqual(partners_with_discounts[1][10], 360000) # Общий объем продаж второго партнера
    
    def test_get_product_type_name(self):
        """Тест функции получения имени типа продукта по ID"""
        product_type_name = db.get_product_type_name(1)
        self.assertEqual(product_type_name, 'Тестовый тип 1')
        
        product_type_name = db.get_product_type_name(2)
        self.assertEqual(product_type_name, 'Тестовый тип 2')
        
        # Тест для несуществующего ID
        product_type_name = db.get_product_type_name(999)
        self.assertEqual(product_type_name, 'Неизвестный тип')

if __name__ == '__main__':
    unittest.main() 