import datetime
import sqlite3
import openpyxl

# wb=openpyxl.load_workbook("Products_import.xlsx")
# sheet=wb.active
# Products_import=[]
# for row in sheet.iter_rows(values_only=1):
#     Products_import.append(row)

# print(Products_import)


path='database.db'

def init_dp():

    connect=sqlite3.connect(path)
    cursor = connect.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS ... (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   ... TEXT NOT NULL,
                   ... REAL
                   )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS ... (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   Material_type TEXT NOT NULL,
                   Material_brak_percent REAL 
                   )''')
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS .... (
                   .. INTEGER PRIMARY KEY AUTOINCREMENT,
                   ... TEXT,
                   ... TEXT NOT NULL,
                   )''')
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS ... (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   . INTEGER NOT NULL,
                   ...
                   ... INTEGER UNIQUE,
                   % REAL,
                   FOREIGN KEY (.) REFERENCES ....(..) ON DELETE RESTRICT
                   )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS ... (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   ..... INTEGER NOT NULL,
                   .... INTEGER NOT NULL,
                   ... INTEGER,
                   ... TEXT,
                   FOREIGN KEY (.....) REFERENCES ...(id) ON DELETE RESTRICT,
                   FOREIGN KEY (....) REFERENCES ...(id) ON DELETE RESTRICT
                   )''')
                   
    connect.commit()
    connect.close()


def add_context():
    connect= sqlite3.connect(path)
    cursor = connect.cursor()

    cursor.executemany("INSERT INTO Product_type_import (type, kaof_type) VALUES (?,?)", 
                      [(item[0], item[1]) for item in ... if item[0] is not None])
    
    # Добавляем партнеров
    cursor.executemany("INSERT INTO Partners_import (type, name, director, male, phone, adress, inn, rate) VALUES (?,?,?,?,?,?,?,?)", 
                      ...)
    
    # Добавляем продукты с правильными ссылками на типы
    for product in ...:
        product_type, name, articul, min_price = product
        
        # Получаем ID типа продукта
        cursor.execute("SELECT id FROM Product_type_import WHERE type = ?", (product_type,))
        type_id = cursor.fetchone()
        
        if type_id:
            cursor.execute("INSERT INTO Products_import (type_id, Name, articul, min_price) VALUES (?,?,?,?)", 
                         (type_id[0], name, articul, min_price))
    
    # Добавляем продукты партнеров с правильными ссылками
    for partner_product in ...:
        prod_name, partner_name, value, data = partner_product
        # Получаем ID продукта
        cursor.execute("SELECT id FROM Products_import WHERE Name = ?", (prod_name,))
        product_id = cursor.fetchone()
        
        # Получаем ID партнера
        cursor.execute("SELECT id FROM Partners_import WHERE name = ?", (partner_name,))
        partner_id = cursor.fetchone()
        
        if product_id and partner_id:
            data_str = data.isoformat() if hasattr(data, 'isoformat') else str(data)
            cursor.execute("INSERT INTO Partner_products_import (product_id, partner_id, Value, Data) VALUES (?,?,?,?)", 
                         (product_id[0], partner_id[0], value, data_str))
    
    cursor.executemany("INSERT INTO ... (Material_type, Material_brak_percent) VALUES (?,?)", 
                      )
    
    connect.commit()
    connect.close()


# def get_partners():
#     connect = sqlite3.connect(path)
#     cursor = connect.cursor()
#     cursor.execute("SELECT * FROM Partners_import")
#     result = cursor.fetchall()
#     connect.close()
#     return result
    
# def add_product_type_import(pdtype, kaof_type):
#     conn= sqlite3.connect(path)
#     cursor = conn.cursor()
#     try:
#         cursor.execute("INSERT INTO Product_type_import (type, kaof_type) VALUES (?,?)", (pdtype, kaof_type))
#     except Exception as e:
#         print("Ошибка при работе функции add_product_type_import", e)
#     conn.commit()
#     conn.close()


# def calculate_partner_discount(partner_id):
   
#     conn = sqlite3.connect(path)
#     cursor = conn.cursor()
    
#     cursor.execute("""
#         SELECT SUM(Value) 
#         FROM Partner_products_import 
#         WHERE partner_id = ?
#     """, (partner_id,))
    
#     result = cursor.fetchone()
#     total_sales = result[0] if result[0] is not None else 0
#     conn.close()
    
   
#     if total_sales < 10000:
#         return 0
#     elif 10000 <= total_sales < 50000:
#         return 5
#     elif 50000 <= total_sales < 300000:
#         return 10
#     else: 
#         return 15

# def get_partner_total_sales(partner_id):
#     conn = sqlite3.connect(path)
#     cursor = conn.cursor()
    
#     cursor.execute("""
#         SELECT SUM(Value) 
#         FROM Partner_products_import 
#         WHERE partner_id = ?
#     """, (partner_id,))
    
#     result = cursor.fetchone()
#     conn.close()
#     return result[0] if result[0] is not None else 0

# def get_partners_with_discounts():
#     partners = get_partners()
#     result = []
    
#     for partner in partners:
#         partner_id = partner[0]
#         discount = calculate_partner_discount(partner_id)
#         total_sales = get_partner_total_sales(partner_id)
        
#         partner_with_discount = list(partner)
#         partner_with_discount.append(discount)
#         partner_with_discount.append(total_sales)
#         result.append(tuple(partner_with_discount))
    
#     return result

# def delete_product_type(id):
#     conn = sqlite3.connect(path)
#     cursor = conn.cursor()
#     cursor.execute("DELETE FROM Product_type_import WHERE id = ?", (id,))
#     conn.commit()
#     conn.close()



# def update_product_type(id, type_value, kaof_value):
#     conn = sqlite3.connect(path)
#     cursor = conn.cursor()
#     cursor.execute("UPDATE Product_type_import SET type = ?, kaof_type = ? WHERE id = ?", 
#                   (type_value, kaof_value, id))
#     conn.commit()
#     conn.close()

# def add_partner(org_type, name, director, email, phone, address, inn, rate):
#     conn = sqlite3.connect(path)
#     cursor = conn.cursor()
#     try:
#         cursor.execute(
#             "INSERT INTO Partners_import (type, name, director, male, phone, adress, inn, rate) VALUES (?,?,?,?,?,?,?,?)",
#             (org_type, name, director, email, phone, address, inn, rate)
#         )
#         conn.commit()
#     except Exception as e:
#         print(f"Ошибка при добавлении партнера: {e}")
#     finally:
#         conn.close()



