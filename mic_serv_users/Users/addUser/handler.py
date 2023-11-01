try:
  import unzip_requirements
except ImportError:
  pass
import json, os, jwt
from pymongo import MongoClient
from bson import ObjectId
from passlib.hash import pbkdf2_sha256

conn = MongoClient(os.environ.get('MONGO_URI'))
secret = os.environ.get("JWT_SECRET")
db = conn.mic_serv_users

def addUser(event, context):
    """
    The `addUser` function is used to add a new user to the database, encrypting their password and
    returning a success message.
    
    :param event: The `event` parameter is a dictionary that contains information about the event that
    triggered the function. It typically includes details such as the HTTP request headers, body, and
    other relevant information
    :param context: The `context` parameter is an object that provides information about the runtime
    environment of the function. It includes details such as the AWS request ID, function name, and
    other contextual information. In this code snippet, the `context` parameter is not used, so it can
    be removed from the function signature
    :return: a response object with a status code of 201 (indicating a successful creation) and a body
    containing a JSON message indicating that the user with the specified ID was created successfully.
    """
    users = db.users
    dependents = db.dependents
    user_id = getUserIdByToken(event['headers']['Authorization'])
    user_data = json.loads(event['body'])
    password = pbkdf2_sha256.hash(user_data['password'])
    del user_data['password']
    user_data['isUser'] = True
    user_data['user_id'] = user_id
    dependents.insert_one(user_data)
    users.update_one({'_id':ObjectId(user_id)}, {"$set": {'password': password}}, upsert=False)
    body = json.dumps( { 'message' : f"user with ID {user_id} was created successfully"}) 
    response = {
        'statusCode': 201,
        'headers': {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Credentials': True,
        },
        'body': body
    }
    return response

def getUserIdByToken(token):
    token = token.replace("Bearer ", "")
    user_info = jwt.decode(token, secret, algorithms=["HS256"])
    return user_info['_id']
