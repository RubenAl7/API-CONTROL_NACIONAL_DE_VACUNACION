try:
  import unzip_requirements
except ImportError:
  pass
from datetime import datetime, timedelta
import json, os
from pymongo import MongoClient
import jwt

conn = MongoClient(os.environ.get('MONGO_URI'))
secret = os.environ.get('JWT_SECRET')

def checkCode(event, context):
    """
    The `checkCode` function checks if a given code matches the code associated with a user's phone
    number and returns a response accordingly.
    
    :param event: The `event` parameter is a dictionary that contains information about the event that
    triggered the function. It typically includes details such as the HTTP request headers, body, and
    other metadata
    :param context: The `context` parameter in the `checkCode` function is typically used to provide
    information about the runtime environment of the function. It can include details such as the AWS
    Lambda function name, version, memory limit, and other contextual information. However, in the
    provided code snippet, the `context`
    :return: a response object with a status code and a body. The status code indicates the success or
    failure of the code check, and the body contains a message and possibly a token.
    """
    body = json.loads(event['body'])
    phone = body['phone']
    code = body['code']
    db = conn.mic_serv_users
    users = db.users
    user = users.find_one({"phone": phone})
    if user:
        if int(code) == int(user['last_code']):
            exp_time = datetime.now() + timedelta(minutes=5)
            token = jwt.encode({'_id':str(user['_id']), 'exp': exp_time}, secret, algorithm="HS256")
            users.update_one({'_id':user['_id']}, {"$set": {'status': 'verified', 'token': token}}, upsert=False)
            body = json.dumps( { 'message' : f"Code was checked successfully. Proceed with registration", 
                                 'token': token
                                }) 
            response = {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Credentials': True,
                },
                'body': body
            }
        else:
            body = json.dumps( { 'message' : f"Code was incorrect. Try again or request a new code"}) 
            response = {
                'statusCode': 401,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Credentials': True,
                },
                'body': body
            }
    else:
        body = json.dumps( { 'message' : f"Error validating user. Please try again."}) 
        response = {
            'statusCode': 404,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': True,
            },
            'body': body
        }
    return response

