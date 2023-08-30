from flask import Blueprint, jsonify, request
from database import database
import controllers.user_controller as user_controller
from helpers.token_validation import validateToken

user = Blueprint("user", __name__)

@user.route("/v0/users/signup", methods=["POST"])
def create():
    data = request.get_json()

    if 'email' not in data or 'password' not in data or 'name' not in data:
        return jsonify({'error': "Email, password, and name are required fields!"}), 400


    createdUser = user_controller.CreateUser(data)


    if createdUser == "Duplicated User":
        return jsonify({'error': "Email Already Exists"}), 400

    if not createdUser.inserted_id:
        return jsonify({'error': "Something went wrong!"}), 400

    return jsonify({'id': str(createdUser.inserted_id)}), 201


@user.route("/v0/users/login", methods=["POST"])
def login():
    data = request.get_json()

    if 'email' not in data or 'password' not in data:
        return jsonify({'error': "Email and password are required fields!"}), 400

    loginAttempt = user_controller.loginUser(data)

    if loginAttempt == "Invalid email" or loginAttempt == "Invalid Password":
        return jsonify({'error': "Invalid Email or Password"}), 401

    return jsonify({
        'token': loginAttempt.json['token'],
        'expiration': loginAttempt.json['expiration'],
        'loggedUser': loginAttempt.json['loggedUser']
    })


@user.route("/v0/users/all", methods=["GET"])
def fetch():
    token = validateToken()

    if token == 400:
        return jsonify({'error': "Token is missing"}), 400
    elif token == 401:
        return jsonify({'error': "Invalid Auth"}), 401

    try:
        return user_controller.fetchUsers()
    except Exception as e:
        return jsonify({'error': "Error on fetching users: " + str(e)}), 500
