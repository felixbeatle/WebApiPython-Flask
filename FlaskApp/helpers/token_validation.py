
from flask import request
import jwt
import app_config as config

def validateToken():
    token = None
    userInformation = None

    try:
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        
        if not token:
            return 400
        
        try:
            userInformation = jwt.decode(token, key=config.TOKEN_SECRET, algorithms=["HS256"])
            print(userInformation)
        except Exception:
            return 401
        
        return userInformation
    except:
        return 400
