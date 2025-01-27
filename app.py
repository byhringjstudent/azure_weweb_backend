# this file is reserved for the Flask App file

from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# Database configuration
db_config = {
    'host': 'your_azure_postgresql_host',
    'dbname': 'your_database_name',
    'user': 'your_username',
    'password': 'your_password',
    'port': 5432
}

# Establish a database connection
def get_db_connection():
    try:
        connection = psycopg2.connect(
            host=db_config['host'],
            dbname=db_config['dbname'],
            user=db_config['user'],
            password=db_config['password'],
            port=db_config['port'],
            cursor_factory=RealDictCursor
        )
        return connection
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

# Define API routes
@app.route('/api/data', methods=['GET'])
def get_data():
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({'error': 'Database connection failed'}), 500

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM your_table_name;")
        data = cursor.fetchall()
        cursor.close()
        connection.close()

        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/data', methods=['POST'])
def insert_data():
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({'error': 'Database connection failed'}), 500

        new_data = request.json
        cursor = connection.cursor()
        query = "INSERT INTO your_table_name (column1, column2) VALUES (%s, %s) RETURNING id;"
        values = (new_data['column1'], new_data['column2'])
        cursor.execute(query, values)
        inserted_id = cursor.fetchone()['id']
        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({'id': inserted_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/data/<int:data_id>', methods=['PUT'])
def update_data(data_id):
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({'error': 'Database connection failed'}), 500

        update_data = request.json
        cursor = connection.cursor()
        query = "UPDATE your_table_name SET column1 = %s, column2 = %s WHERE id = %s;"
        values = (update_data['column1'], update_data['column2'], data_id)
        cursor.execute(query, values)
        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({'message': 'Data updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/data/<int:data_id>', methods=['DELETE'])
def delete_data(data_id):
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({'error': 'Database connection failed'}), 500

        cursor = connection.cursor()
        query = "DELETE FROM your_table_name WHERE id = %s;"
        cursor.execute(query, (data_id,))
        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({'message': 'Data deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
