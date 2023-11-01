try:
  import unzip_requirements
except ImportError:
  pass
from datetime import datetime, timedelta
import json, os, jwt
from pymongo import MongoClient
from bson import ObjectId
from passlib.hash import pbkdf2_sha256

conn = MongoClient(os.environ.get('MONGO_URI'))
secret = os.environ.get("JWT_SECRET")
db = conn.mic_serv_users

def login(event, context):
    """
    The `login` function takes in user data, validates it, and returns a response with a token if the
    user is validated successfully, otherwise it returns an unauthorized response.
    
    :param event: The `event` parameter is a dictionary that contains information about the event that
    triggered the function. In this case, it is expected to have a key called `'body'` which contains
    the request body as a JSON string
    :param context: The `context` parameter in the `login` function is a context object that provides
    information about the runtime environment of the function. It includes properties such as the AWS
    request ID, the function name, the function version, and more. The `context` object is automatically
    passed to the function by the
    :return: The code is returning a response object with a status code and a body. If the user is
    validated successfully, it returns a response with a status code of 200 and a body containing a
    message and a token. If the user is not validated, it returns a response with a status code of 401
    and a body containing the message "Unauthorized".
    """
    udata = json.loads(event['body'])
    isVal, id = validateUser(udata['ci'], udata['password'])
    if (isVal):
        exp_time = datetime.now() + timedelta(minutes=5)
        token = jwt.encode({"_id": str(id), 'exp': exp_time}, secret, algorithm="HS256")
        body = json.dumps( { 'message' : f"user validated successfully", "token": token}) 
        response = {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': True,
            },
            'body': body
        }
        return response
    response = {
        'statusCode': 401,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True,
        },
        'body': "Unauthorized"
    }
    return response

def validateUser(ci, password):
    users = db.users
    user = users.find_one({"ci": ci}) 
    if (pbkdf2_sha256.verify(password, user['password'])):
       return True, user['_id']
    return False, False