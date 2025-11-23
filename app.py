from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to DevSecOps Pipeline!",
        "version": "1.0.0",
        "status": "healthy"
    })

@app.route('/health')
def health():
    return jsonify({"status": "UP"}), 200

@app.route('/api/users')
def get_users():
    users = [
        {"id": 1, "name": "John Doe", "email": "john@example.com"},
        {"id": 2, "name": "Jane Smith", "email": "jane@example.com"}
    ]
    return jsonify(users)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
