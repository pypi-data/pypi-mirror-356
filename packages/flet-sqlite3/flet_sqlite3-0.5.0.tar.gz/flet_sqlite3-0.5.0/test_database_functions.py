import unittest
import sqlite3
import os
import database as db

class TestDatabaseFunctions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_db_path = "test_db_functions.db"
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

    def test_update_partner(self):
        """Тест обновления информации о партнере"""
        # Добавляем тестового партнера
        db.add_partner(
            "ООО", "Тест Партнер Обновление", "Тестов Тест Тестович", 
            "test@test.ru", "123-456-789", "Тестовая улица, 1", 
            "1111111111", 5
        )
        
        # Получаем ID добавленного партнера
        conn = sqlite3.connect(self.test_db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM Partners_import WHERE name = ?", ("Тест Партнер Обновление",))
        partner_id = cursor.fetchone()[0]
        conn.close()
        
        # Обновляем информацию о партнере
        db.update_partner(
            partner_id, "ЗАО", "Тест Партнер Обновленный", "Иванов Иван Иванович", 
            "new@test.ru", "987-654-321", "Новая улица, 10", 
            "2222222222", 8
        )
        
        # Получаем обновленную информацию о партнере
        conn = sqlite3.connect(self.test_db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Partners_import WHERE id = ?", (partner_id,))
        updated_partner = cursor.fetchone()
        conn.close()
        
        # Проверяем, что информация обновлена корректно
        self.assertEqual(updated_partner[1], "ЗАО")
        self.assertEqual(updated_partner[2], "Тест Партнер Обновленный")
        self.assertEqual(updated_partner[3], "Иванов Иван Иванович")
        self.assertEqual(updated_partner[4], "new@test.ru")
        self.assertEqual(updated_partner[5], "987-654-321")
        self.assertEqual(updated_partner[6], "Новая улица, 10")
        self.assertEqual(updated_partner[7], "2222222222")
        self.assertEqual(updated_partner[8], 8)

    def test_delete_partner(self):
        """Тест удаления партнера"""
        # Добавляем тестового партнера
        db.add_partner(
            "ООО", "Тест Партнер Удаление", "Тестов Тест Тестович", 
            "test@test.ru", "123-456-789", "Тестовая улица, 1", 
            "3333333333", 5
        )
        
        # Получаем ID добавленного партнера
        conn = sqlite3.connect(self.test_db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM Partners_import WHERE name = ?", ("Тест Партнер Удаление",))
        partner_id = cursor.fetchone()[0]
        conn.close()
        
        # Удаляем партнера
        db.delete_partner(partner_id)
        
        # Проверяем, что партнер удален
        conn = sqlite3.connect(self.test_db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Partners_import WHERE id = ?", (partner_id,))
        deleted_partner = cursor.fetchone()
        conn.close()
        
        self.assertIsNone(deleted_partner)

    def test_get_product_type_name(self):
        """Тест получения названия типа продукта по ID"""
        # Добавляем тестовый тип продукта
        db.add_product_type_import("Тестовый тип для функции", 2.5)
        
        # Получаем ID добавленного типа продукта
        conn = sqlite3.connect(self.test_db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM Product_type_import WHERE type = ?", ("Тестовый тип для функции",))
        type_id = cursor.fetchone()[0]
        conn.close()
        
        # Получаем название типа продукта по ID
        type_name = db.get_product_type_name(type_id)
        
        # Проверяем, что название получено корректно
        self.assertEqual(type_name, "Тестовый тип для функции")

    def test_get_product_name(self):
        """Тест получения названия продукта по ID"""
        # Добавляем тестовый тип продукта
        db.add_product_type_import("Тестовый тип для продукта", 1.0)
        
        # Получаем ID добавленного типа продукта
        conn = sqlite3.connect(self.test_db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM Product_type_import WHERE type = ?", ("Тестовый тип для продукта",))
        type_id = cursor.fetchone()[0]
        
        # Добавляем тестовый продукт
        cursor.execute("""
            INSERT INTO Products_import (type_id, Name, articul, min_price) 
            VALUES (?, ?, ?, ?)
        """, (type_id, "Тестовый продукт для функции", 54321, 2000.0))
        product_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        # Получаем название продукта по ID
        product_name = db.get_product_name(product_id)
        
        # Проверяем, что название получено корректно
        self.assertEqual(product_name, "Тестовый продукт для функции")

    def test_get_partner_name(self):
        """Тест получения названия партнера по ID"""
        # Добавляем тестового партнера
        db.add_partner(
            "ООО", "Тест Партнер для функции", "Тестов Тест Тестович", 
            "test@test.ru", "123-456-789", "Тестовая улица, 1", 
            "4444444444", 5
        )
        
        # Получаем ID добавленного партнера
        conn = sqlite3.connect(self.test_db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM Partners_import WHERE name = ?", ("Тест Партнер для функции",))
        partner_id = cursor.fetchone()[0]
        conn.close()
        
        # Получаем название партнера по ID
        partner_name = db.get_partner_name(partner_id)
        
        # Проверяем, что название получено корректно
        self.assertEqual(partner_name, "Тест Партнер для функции")

if __name__ == "__main__":
    unittest.main() 