from database.__init__ import database
from models.user_model import User
import bcrypt
import app_config as config
from datetime import datetime, timedelta
import jwt
from flask import jsonify


def generateHashPassword(password):
    salt = bcrypt.gensalt()
    hashPassword = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashPassword

def CreateUser(userInformation):
    try:
        newUser = User()
        newUser.name = userInformation['name'].lower()
        newUser.email = userInformation['email'].lower()
        newUser.password = generateHashPassword(userInformation['password'])

        print(newUser.__dict__)


        collection = database.dataBase[config.CONST_USER_COLLECTION]
        if collection.find_one({'email': newUser.email}):
            return "Duplicated User"

        createdUser = collection.insert_one(newUser.__dict__)
        print("hello3")
        return createdUser
    
    except Exception as err:
        raise ValueError("Error on creating User!", err)

def loginUser(userInformation):
    email = userInformation['email'].lower()
    password = userInformation['password'].encode("utf-8")

    collection = database.dataBase[config.CONST_USER_COLLECTION]

    currentUser = collection.find_one({'email': email})

    if not currentUser:
        return "Invalid Email"

    if not bcrypt.checkpw(password, currentUser["password"]):
        return "Invalid Password"
    
    loggedUser = {}
    loggedUser['uid'] = str(currentUser['_id'])
    loggedUser['email'] = currentUser['email']
    loggedUser['name'] = currentUser['name']

    expiration = datetime.utcnow() + timedelta(seconds = config.JWT_EXPIRATION)

    jwtData = {'email': currentUser['email'], 'id': str(currentUser['_id']), 'exp': expiration}

    jwtToReturn = jwt.encode(payload = jwtData, key = config.TOKEN_SECRET)

    return jsonify({'token': jwtToReturn, 'expiration': config.JWT_EXPIRATION, 'loggedUser': loggedUser})

def fetchUsers():

    collection = database.dataBase[config.CONST_USER_COLLECTION]
    users = []

    for item in collection.find():
        currentUser = {}
        currentUser["uid"] = str(item["_id"])
        currentUser["email"] = item["email"]
        currentUser["name"] = item["name"]
        users.append(currentUser)
    print(users)
    return jsonify({"users": users})

