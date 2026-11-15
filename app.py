from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)  # Taake browser se requests allow ho

# MySQL Database Connection
def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # XAMPP mein default password khaali hota hai
        database="portfolio_db"
    )
    return connection

# Contact form submit karne wala route
@app.route('/submit-contact', methods=['POST'])
def submit_contact():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')

    if not name or not email or not message:
        return jsonify({"error": "All fields are required"}), 400

    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO contacts (name, email, message) VALUES (%s, %s, %s)",
            (name, email, message)
        )
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({"success": True, "message": "Message saved successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)