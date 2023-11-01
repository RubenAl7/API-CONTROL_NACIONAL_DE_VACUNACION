try:
  import unzip_requirements
except ImportError:
  pass
import json, os, jwt
from pymongo import MongoClient

conn = MongoClient(os.environ.get('MONGO_URI'))
secret = os.environ.get("JWT_SECRET")
db = conn.mic_serv_users

def addDependent(event, context):
    """
    The function `addDependent` adds a dependent of an user to the database and returns a response
    indicating success.
    
    :param event: The `event` parameter is a dictionary that contains information about the event that
    triggered the function. It typically includes details such as the HTTP request body, headers, and
    other relevant data
    :param context: The `context` parameter is an object that provides information about the runtime
    environment of the function. It includes details such as the AWS request ID, function name, and
    memory limit. It can be used to access information about the execution environment or to interact
    with AWS services. In this code snippet, the
    :return: a response object with a status code of 201 (indicating a successful creation) and a body
    containing a JSON message indicating that the dependent was added successfully.
    """
    dependents = db.dependents
    dependent_data = json.loads(event['body'])
    dependent_data['user_id'] = getUserIdByToken(event['headers']['Authorization'])
    dependent_data['isUser'] = False
    dependents.insert_one(dependent_data)
    body = json.dumps( { 'message' : f"Dependent was added successfully"}) 
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
