import unittest
import sqlite3
import os
import sys
import database as db
from unittest.mock import patch

class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_db_path = "test_db.db"
        # Сохраняем оригинальный путь к базе данных
        cls.original_path = db.path
        # Устанавливаем тестовый путь к базе данных
        db.path = cls.test_db_path
        # Инициализируем тестовую базу данных
        db.init_dp()

    @classmethod
    def tearDownClass(cls):
        # Восстанавливаем оригинальный путь к базе данных
        db.path = cls.original_path
        # Удаляем тестовую базу данных
        if os.path.exists(cls.test_db_path):
            try:
                os.remove(cls.test_db_path)
            except PermissionError:
                print(f"Не удалось удалить {cls.test_db_path}: файл занят другим процессом")

    def setUp(self):
        # Перед каждым тестом закрываем все соединения
        conn = sqlite3.connect(self.test_db_path)
        conn.close()

    def tearDown(self):
        # После каждого теста закрываем все соединения
        conn = sqlite3.connect(self.test_db_path)
        conn.close()

    def test_add_and_get_product_type(self):
        """Тест добавления и получения типа продукта"""
        # Добавляем тестовый тип продукта
        db.add_product_type_import("Тестовый тип", 1.5)
        
        # Получаем все типы продуктов
        product_types = db.get_product_type_import()
        
        # Проверяем, что наш тип продукта добавлен
        found = False
        for product_type in product_types:
            if product_type[1] == "Тестовый тип" and product_type[2] == 1.5:
                found = True
                break
        
        self.assertTrue(found, "Тип продукта не был добавлен или получен корректно")

    def test_add_and_get_material_type(self):
        """Тест добавления и получения типа материала"""
        # Добавляем тестовый тип материала через прямой SQL-запрос
        conn = sqlite3.connect(self.test_db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Material_type_import (Material_type, Material_brak_percent) VALUES (?, ?)",
            ("Тестовый материал", 0.25)
        )
        conn.commit()
        conn.close()
        
        # Получаем все типы материалов
        material_types = db.get_material_type_import()
        
        # Проверяем, что наш тип материала добавлен
        found = False
        for material_type in material_types:
            if material_type[1] == "Тестовый материал" and material_type[2] == 0.25:
                found = True
                break
        
        self.assertTrue(found, "Тип материала не был добавлен или получен корректно")

    def test_add_and_get_partner(self):
        """Тест добавления и получения партнера"""
        # Добавляем тестового партнера
        db.add_partner(
            "ООО", "Тест Партнер", "Тестов Тест Тестович", 
            "test@test.ru", "123-456-789", "Тестовая улица, 1", 
            "1234567890", 5
        )
        
        # Получаем всех партнеров
        partners = db.get_partners()
        
        # Проверяем, что наш партнер добавлен
        found = False
        for partner in partners:
            if partner[2] == "Тест Партнер" and partner[3] == "Тестов Тест Тестович":
                found = True
                break
        
        self.assertTrue(found, "Партнер не был добавлен или получен корректно")

    def test_calculate_partner_discount(self):
        """Тест расчета скидки партнера на основе объема продаж"""
        # Добавляем тестового партнера
        db.add_partner(
            "ООО", "Тест Партнер Скидка", "Тестов Тест Тестович", 
            "test@test.ru", "123-456-789", "Тестовая улица, 1", 
            "9876543210", 5
        )
        
        # Получаем ID добавленного партнера
        conn = sqlite3.connect(self.test_db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM Partners_import WHERE name = ?", ("Тест Партнер Скидка",))
        partner_id = cursor.fetchone()[0]
        
        # Добавляем тестовый тип продукта
        cursor.execute("INSERT INTO Product_type_import (type, kaof_type) VALUES (?, ?)", ("Тестовый тип для скидки", 1.0))
        type_id = cursor.lastrowid
        
        # Добавляем тестовый продукт
        cursor.execute("INSERT INTO Products_import (type_id, Name, articul, min_price) VALUES (?, ?, ?, ?)", 
                      (type_id, "Тестовый продукт для скидки", 12345, 1000.0))
        product_id = cursor.lastrowid
        
        # Добавляем продажи партнера с разными объемами для проверки разных уровней скидок
        test_cases = [
            (5000, 0),    # Объем < 10000 => скидка 0%
            (20000, 5),   # 10000 <= Объем < 50000 => скидка 5%
            (100000, 10), # 50000 <= Объем < 300000 => скидка 10%
            (350000, 15)  # Объем >= 300000 => скидка 15%
        ]
        
        for sales_volume, expected_discount in test_cases:
            # Очищаем предыдущие продажи
            cursor.execute("DELETE FROM Partner_products_import WHERE partner_id = ?", (partner_id,))
            
            # Добавляем продажу с текущим объемом
            cursor.execute(
                "INSERT INTO Partner_products_import (product_id, partner_id, Value, Data) VALUES (?, ?, ?, ?)",
                (product_id, partner_id, sales_volume, "2023-01-01")
            )
            conn.commit()
            
            # Проверяем расчет скидки
            discount = db.calculate_partner_discount(partner_id)
            self.assertEqual(discount, expected_discount, 
                            f"Неверный расчет скидки для объема {sales_volume}: ожидалось {expected_discount}%, получено {discount}%")
        
        conn.close()

    def test_get_partners_with_discounts(self):
        """Тест получения партнеров с рассчитанными скидками"""
        # Добавляем тестового партнера
        db.add_partner(
            "ООО", "Тест Партнер Дисконт", "Тестов Тест Тестович", 
            "test@test.ru", "123-456-789", "Тестовая улица, 1", 
            "5555555555", 5
        )
        
        conn = sqlite3.connect(self.test_db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM Partners_import WHERE name = ?", ("Тест Партнер Дисконт",))
        partner_id = cursor.fetchone()[0]
        
        # Добавляем тестовый тип продукта если его еще нет
        cursor.execute("SELECT id FROM Product_type_import WHERE type = ?", ("Тестовый тип для дисконта",))
        type_id = cursor.fetchone()
        if not type_id:
            cursor.execute("INSERT INTO Product_type_import (type, kaof_type) VALUES (?, ?)", ("Тестовый тип для дисконта", 1.0))
            type_id = cursor.lastrowid
        else:
            type_id = type_id[0]
        
        # Добавляем тестовый продукт если его еще нет
        cursor.execute("SELECT id FROM Products_import WHERE Name = ?", ("Тестовый продукт для дисконта",))
        product_id = cursor.fetchone()
        if not product_id:
            cursor.execute("INSERT INTO Products_import (type_id, Name, articul, min_price) VALUES (?, ?, ?, ?)", 
                        (type_id, "Тестовый продукт для дисконта", 54321, 2000.0))
            product_id = cursor.lastrowid
        else:
            product_id = product_id[0]
        
        # Добавляем продажу партнера с объемом для 10% скидки
        cursor.execute(
            "INSERT INTO Partner_products_import (product_id, partner_id, Value, Data) VALUES (?, ?, ?, ?)",
            (product_id, partner_id, 100000, "2023-01-01")
        )
        conn.commit()
        conn.close()
        
        # Получаем партнеров со скидками
        partners_with_discounts = db.get_partners_with_discounts()

        found = False
        for partner in partners_with_discounts:
            if partner[2] == "Тест Партнер Дисконт":
                found = True
                # Проверяем, что скидка равна 10% (индекс 9) и объем продаж 100000 (индекс 10)
                self.assertEqual(partner[9], 10, "Неверный расчет скидки для партнера")
                self.assertEqual(partner[10], 100000, "Неверный расчет объема продаж для партнера")
                break
        
        self.assertTrue(found, "Партнер со скидкой не был найден в результатах")

if __name__ == "__main__":
    unittest.main() 