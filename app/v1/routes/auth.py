from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.models.user import User
from app import db

# Define auth Blueprint
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
  data = request.json

  if User.query.filter_by(username= data['username']).first():
    return jsonify({"error": "Username already exist"}), 400

  new_user = User(username=data['username'])
  new_user.set_password(data['password'])

  db.session.add(new_user)
  db.session.commit()

  return jsonify({"message": "User registered successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
  data = request.json
  user = User.query.filter_by(username=data['username']).first()

  if not user or not user.check_password(data['password']):
    return jsonify({"error": "Invalid credentials"}), 401

  access_token = create_access_token(identity=user.id)
  return jsonify({"access_token": access_token}), 200