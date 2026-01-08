from database import get_connection

# Product operations
def add_product(name, price, quantity):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO products (name, price, quantity) VALUES (?, ?, ?)', (name, price, quantity))
    conn.commit()
    conn.close()

def get_all_products():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    conn.close()
    return products

def update_product(product_id, name=None, price=None, quantity=None):
    conn = get_connection()
    cursor = conn.cursor()
    if name:
        cursor.execute('UPDATE products SET name = ? WHERE id = ?', (name, product_id))
    if price:
        cursor.execute('UPDATE products SET price = ? WHERE id = ?', (price, product_id))
    if quantity is not None:
        cursor.execute('UPDATE products SET quantity = ? WHERE id = ?', (quantity, product_id))
    conn.commit()
    conn.close()

def delete_product(product_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
    conn.commit()
    conn.close()
