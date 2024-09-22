from flask import Flask, jsonify, request
import redis
import json
import pymysql
from pymysql.cursors import DictCursor

app = Flask(__name__)

# Redis bağlantısı
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

# MySQL bağlantısı
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='password',
    db='product_db',
    cursorclass=DictCursor
)

# Ürünleri veritabanından çekme ve Redis'ten cache kontrolü
def get_products_from_db():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM products")
        return cursor.fetchall()

@app.route('/products', methods=['GET'])
def get_products():
    products = redis_client.get('products')

    if products:
        return jsonify({'source': 'redis', 'data': json.loads(products)})
    else:
        products = get_products_from_db()
        redis_client.set('products', json.dumps(products))
        return jsonify({'source': 'mysql', 'data': products})

@app.route('/products', methods=['POST'])
def add_product():
    data = request.json
    with connection.cursor() as cursor:
        sql = "INSERT INTO products (name, price, description) VALUES (%s, %s, %s)"
        cursor.execute(sql, (data['name'], data['price'], data['description']))
        connection.commit()
    
    # Cache temizlenir
    redis_client.delete('products')
    
    return jsonify({'message': 'Product added successfully'}), 201

@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    data = request.json
    with connection.cursor() as cursor:
        sql = "UPDATE products SET name=%s, price=%s, description=%s WHERE id=%s"
        cursor.execute(sql, (data['name'], data['price'], data['description'], id))
        connection.commit()

    # Cache temizlenir
    redis_client.delete('products')
    
    return jsonify({'message': 'Product updated successfully'})

@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    with connection.cursor() as cursor:
        sql = "DELETE FROM products WHERE id=%s"
        cursor.execute(sql, (id,))
        connection.commit()

    # Cache temizlenir
    redis_client.delete('products')

    return jsonify({'message': 'Product deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
