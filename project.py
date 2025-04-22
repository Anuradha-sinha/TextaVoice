# @author Robin Rajesh
# @email robinsiva1998@gmail.com
# @create date 2024-01-24 16:14:58
# @modify date 2024-01-24 16:14:58
# @desc Review and Rating Aggregator Backend code


from flask import Flask, render_template, jsonify, request

from flask_cors import CORS  


app = Flask(__name__)
CORS(app)  

# Dummy data for illustration (Replace with your database)
audiobooks = [
    {"id": 1, "title": "Sample book 1", "author": "Author 1", "audio_content": "In a world of magic and mystery, young sorcerer Alaric must unravel ancient secrets to save his realm from impending doom in 'Chronicles of Arcane Realms'"},
    {"id": 2, "title": "Sample book 2", "author": "Author 2", "audio_content": "A gripping psychological thriller, 'Whispers in the Shadows' follows detective Emma Harper as she delves into a series of cryptic messages leading to a dark conspiracy that threatens to shatter her reality."},
]

@app.route('/api/audiobooks')
def get_audiobooks():
    return jsonify(audiobooks)

@app.route('/api/add_audiobook', methods=['POST'])
def add_audiobook():
    try:
        data = request.get_json()

        # Validate required fields
        if 'title' not in data or 'author' not in data or 'audioUrl' not in data:
            return jsonify({"error": "Missing required fields"}), 400

        # Add the new audiobook to the data
        new_audiobook = {
            "id": len(audiobooks) + 1,
            "title": data['title'],
            "author": data['author'],
            "audio_content": data['audioUrl'],
        }
        audiobooks.append(new_audiobook)

        return jsonify({"message": "Audiobook added successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/delete_audiobook/<int:audiobook_id>', methods=['DELETE'])
def delete_audiobook(audiobook_id):
    try:
        global audiobooks
        audiobooks = [audiobook for audiobook in audiobooks if audiobook['id'] != audiobook_id]

        return jsonify({"message": "Audiobook deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

from werkzeug.security import generate_password_hash, check_password_hash 
import re     
# Dummy user database (replace with actual DB later)
users = []

# Password strength checker
def is_strong_password(password):
    return bool(re.match(r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password))

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    if not is_strong_password(password):
        return jsonify({
            "error": "Password must be at least 8 characters, include 1 uppercase letter, 1 number, and 1 special character."
        }), 400

    # Check if user already exists
    if any(user["username"] == username for user in users):
        return jsonify({"error": "User already exists"}), 409

    hashed_password = generate_password_hash(password)
    users.append({"username": username, "password": hashed_password})
    return jsonify({"message": "User registered successfully"}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = next((user for user in users if user["username"] == username), None)
    if user and check_password_hash(user["password"], password):
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401

@app.route('/api/logout', methods=['POST'])
def logout():
    # Since no session is maintained, we just send a success response
    return jsonify({"message": "Logged out successfully"}), 200


if __name__ == "__main__":
    app.run(debug=True)
