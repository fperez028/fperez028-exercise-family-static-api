"""
This module takes care of starting the API Server, loading the DB, and adding the endpoints.
"""

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors as JSON
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# Generate sitemap of all endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# Get all members
@app.route('/members', methods=['GET'])
def get_all_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200

# Get a specific member by ID
@app.route('/members/<int:member_id>', methods=['GET'])
def get_member(member_id):
    member = jackson_family.get_member(member_id)
    if member:
        return jsonify(member), 200
    return jsonify({"error": "Member not found"}), 404

# Add a new member
@app.route('/members', methods=['POST'])
def add_member():
    try:
        member_data = request.get_json()
        if not member_data or "first_name" not in member_data or "age" not in member_data or "lucky_numbers" not in member_data:
            return jsonify({"error": "Missing required fields"}), 400
        jackson_family.add_member(member_data)
        return jsonify({"message": "Member added successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Delete a member by ID
@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    deleted = jackson_family.delete_member(member_id)
    if deleted:
        return jsonify({"done": True}), 200
    return jsonify({"error": "Member not found"}), 404

# Run the app
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)