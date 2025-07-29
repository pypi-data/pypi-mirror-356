import unittest
import sqlite3
import os
import database as db
from datetime import datetime

class TestDiscountLogic(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # Создаем тестовую базу данных
        cls.test_db_path = 'test_discount_logic.db'
        # Сохраняем оригинальный путь к базе данных
        cls.original_path = db.path
        # Устанавливаем путь к тестовой базе данных
        db.path = cls.test_db_path
        # Инициализируем базу данных
        db.init_dp()
    
    @classmethod
    def tearDownClass(cls):
        # Возвращаем оригинальный путь к базе данных
        db.path = cls.original_path
        # Удаляем тестовую базу данных
        if os.path.exists(cls.test_db_path):
            os.remove(cls.test_db_path)
    
    def setUp(self):
        # Очищаем базу данных перед каждым тестом
        conn = sqlite3.connect(self.test_db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Partner_products_import")
        cursor.execute("DELETE FROM Products_import")
        cursor.execute("DELETE FROM Partners_import")
        cursor.execute("DELETE FROM Product_type_import")
        conn.commit()
        conn.close()
        
        # Добавляем базовые данные для тестов
        self._add_base_data()
    
    def _add_base_data(self):
        conn = sqlite3.connect(self.test_db_path)
        cursor = conn.cursor()
        
        # Добавляем тип продукта
        cursor.execute("INSERT INTO Product_type_import (type, kaof_type) VALUES (?, ?)", ('Тестовый тип', 1.0))
        product_type_id = cursor.lastrowid
        
        # Добавляем продукт
        cursor.execute("INSERT INTO Products_import (type_id, Name, articul, min_price) VALUES (?, ?, ?, ?)", 
                     (product_type_id, 'Тестовый продукт', 12345, 1000.0))
        product_id = cursor.lastrowid
        
        # Добавляем партнеров для разных сценариев скидок
        partner_data = [
            ('ООО', 'Партнер без скидки', 'Директор 1', 'mail1@test.ru', '111111', 'Адрес 1', '1111111111', 5),
            ('ООО', 'Партнер со скидкой 5%', 'Директор 2', 'mail2@test.ru', '222222', 'Адрес 2', '2222222222', 5),
            ('ООО', 'Партнер со скидкой 10%', 'Директор 3', 'mail3@test.ru', '333333', 'Адрес 3', '3333333333', 5),
            ('ООО', 'Партнер со скидкой 15%', 'Директор 4', 'mail4@test.ru', '444444', 'Адрес 4', '4444444444', 5)
        ]
        
        cursor.executemany("INSERT INTO Partners_import (type, name, director, male, phone, adress, inn, rate) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
                         partner_data)
        
        # Получаем ID добавленных партнеров
        cursor.execute("SELECT id FROM Partners_import ORDER BY id")
        partner_ids = [row[0] for row in cursor.fetchall()]
        
        # Добавляем продажи для каждого партнера с разными объемами
        partner_products_data = [
            (product_id, partner_ids[0], 9000, datetime.now().isoformat()),  # Меньше 10000 - скидка 0%
            (product_id, partner_ids[1], 30000, datetime.now().isoformat()), # От 10000 до 50000 - скидка 5%
            (product_id, partner_ids[2], 100000, datetime.now().isoformat()), # От 50000 до 300000 - скидка 10%
            (product_id, partner_ids[3], 500000, datetime.now().isoformat())  # Более 300000 - скидка 15%
        ]
        
        cursor.executemany("INSERT INTO Partner_products_import (product_id, partner_id, Value, Data) VALUES (?, ?, ?, ?)", 
                         partner_products_data)
        
        conn.commit()
        conn.close()
    
    def test_discount_calculation_no_discount(self):
        """Тест расчета скидки для партнера с объемом продаж менее 10000"""
        # Получаем ID партнера "Партнер без скидки"
        conn = sqlite3.connect(self.test_db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM Partners_import WHERE name = ?", ('Партнер без скидки',))
        partner_id = cursor.fetchone()[0]
        conn.close()
        
        # Проверяем расчет скидки
        discount = db.calculate_partner_discount(partner_id)
        self.assertEqual(discount, 0)
    
    def test_discount_calculation_5_percent(self):
        """Тест расчета скидки для партнера с объемом продаж от 10000 до 50000"""
        # Получаем ID партнера "Партнер со скидкой 5%"
        conn = sqlite3.connect(self.test_db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM Partners_import WHERE name = ?", ('Партнер со скидкой 5%',))
        partner_id = cursor.fetchone()[0]
        conn.close()
        
        # Проверяем расчет скидки
        discount = db.calculate_partner_discount(partner_id)
        self.assertEqual(discount, 5)
    
    def test_discount_calculation_10_percent(self):
        """Тест расчета скидки для партнера с объемом продаж от 50000 до 300000"""
        # Получаем ID партнера "Партнер со скидкой 10%"
        conn = sqlite3.connect(self.test_db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM Partners_import WHERE name = ?", ('Партнер со скидкой 10%',))
        partner_id = cursor.fetchone()[0]
        conn.close()
        
        # Проверяем расчет скидки
        discount = db.calculate_partner_discount(partner_id)
        self.assertEqual(discount, 10)
    
    def test_discount_calculation_15_percent(self):
        """Тест расчета скидки для партнера с объемом продаж более 300000"""
        # Получаем ID партнера "Партнер со скидкой 15%"
        conn = sqlite3.connect(self.test_db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM Partners_import WHERE name = ?", ('Партнер со скидкой 15%',))
        partner_id = cursor.fetchone()[0]
        conn.close()
        
        # Проверяем расчет скидки
        discount = db.calculate_partner_discount(partner_id)
        self.assertEqual(discount, 15)
    
    def test_discount_calculation_boundary_values(self):
        """Тест расчета скидки для граничных значений объемов продаж"""
        # Создаем партнеров с граничными значениями объемов продаж
        conn = sqlite3.connect(self.test_db_path)
        cursor = conn.cursor()
        
        # Добавляем тип продукта и продукт, если их еще нет
        cursor.execute("SELECT id FROM Product_type_import LIMIT 1")
        product_type_id = cursor.fetchone()[0]
        
        cursor.execute("SELECT id FROM Products_import LIMIT 1")
        product_id = cursor.fetchone()[0]
        
        # Добавляем партнеров для тестирования граничных значений
        boundary_partners = [
            ('ООО', 'Граничное значение 1', 'Директор', 'mail@test.ru', '111111', 'Адрес', '1111111112', 5),  # 10000 ровно
            ('ООО', 'Граничное значение 2', 'Директор', 'mail@test.ru', '222222', 'Адрес', '2222222223', 5),  # 50000 ровно
            ('ООО', 'Граничное значение 3', 'Директор', 'mail@test.ru', '333333', 'Адрес', '3333333334', 5)   # 300000 ровно
        ]
        
        cursor.executemany("INSERT INTO Partners_import (type, name, director, male, phone, adress, inn, rate) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
                         boundary_partners)
        
        # Получаем ID добавленных партнеров
        cursor.execute("SELECT id FROM Partners_import WHERE name LIKE 'Граничное значение%'")
        boundary_partner_ids = [row[0] for row in cursor.fetchall()]
        
        # Добавляем продажи для каждого партнера с граничными значениями
        boundary_sales = [
            (product_id, boundary_partner_ids[0], 10000, datetime.now().isoformat()),  # Ровно 10000 - скидка 5%
            (product_id, boundary_partner_ids[1], 50000, datetime.now().isoformat()),  # Ровно 50000 - скидка 10%
            (product_id, boundary_partner_ids[2], 300000, datetime.now().isoformat())  # Ровно 300000 - скидка 15%
        ]
        
        cursor.executemany("INSERT INTO Partner_products_import (product_id, partner_id, Value, Data) VALUES (?, ?, ?, ?)", 
                         boundary_sales)
        
        conn.commit()
        conn.close()
        
        # Проверяем расчет скидок для граничных значений
        self.assertEqual(db.calculate_partner_discount(boundary_partner_ids[0]), 5)  # 10000 -> 5%
        self.assertEqual(db.calculate_partner_discount(boundary_partner_ids[1]), 10) # 50000 -> 10%
        self.assertEqual(db.calculate_partner_discount(boundary_partner_ids[2]), 15) # 300000 -> 15%

if __name__ == '__main__':
    unittest.main() 