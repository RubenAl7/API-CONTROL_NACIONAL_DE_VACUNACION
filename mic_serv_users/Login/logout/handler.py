try:
  import unzip_requirements
except ImportError:
  pass
import json, os, jwt
from pymongo import MongoClient

conn = MongoClient(os.environ.get('MONGO_URI'))
secret = os.environ.get("JWT_SECRET")
db = conn.mic_serv_users

def logout(event, context):
    """
    The `logout` function logs out a user by adding their token to a blacklist and returning a success
    message, or returns an unauthorized error message if the user is not authenticated.
    
    :param event: The `event` parameter is a dictionary that contains information about the event that
    triggered the function. In this case, it likely contains information about the HTTP request that was
    made to the function
    :param context: The `context` parameter is an object that provides information about the runtime
    environment of the function. It includes details such as the AWS request ID, function name, and
    other contextual information. In this code snippet, the `context` parameter is not used, so it can
    be safely ignored
    :return: a response object. If the user is authenticated, it returns a response with a status code
    of 200 and a message indicating that the logout was successful. If the user is not authenticated, it
    returns a response with a status code of 401 and a message indicating that the request is
    unauthorized.
    """
    blacklist = db.token_blacklist
    user = getUserIdByToken(event['headers']['Authorization'])
    if (user):
        to_blacklist = {"token": event['headers']['Authorization'], "user_id": user}
        blacklist.insert_one(to_blacklist)
        body = json.dumps( { 'message' : f"Logout made successfully"}) 
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

def getUserIdByToken(token):
    token = token.replace("Bearer ", "")
    user_info = jwt.decode(token, secret, algorithms=["HS256"])
    return user_info['_id']