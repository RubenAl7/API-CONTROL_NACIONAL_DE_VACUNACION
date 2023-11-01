try:
  import unzip_requirements
except ImportError:
  pass
import os, jwt
from pymongo import MongoClient

conn = MongoClient(os.environ.get('MONGO_URI'))
secret = os.environ.get("JWT_SECRET")
db = conn.mic_serv_users

def verifyToken(event, context):
    """
    The `verifyToken` function checks if a token is valid and not blacklisted, and generates a policy
    document for authorization.
    
    :param event: The `event` parameter is a dictionary that contains information about the event that
    triggered the function. It typically includes details such as the HTTP request headers, body, and
    other relevant information
    :param context: The `context` parameter is an object that provides information about the runtime
    environment of the function. It includes details such as the AWS request ID, function name, and
    other contextual information. In this code snippet, the `context` parameter is not used, so it can
    be removed from the function signature
    :return: a dictionary with two keys: 'principalId' and 'policyDocument'. The value of 'principalId'
    can be either 'unauthorized' or the user's ID. The value of 'policyDocument' is generated based on
    the result of the verification process and can be either 'Allow' or 'Deny'.
    """
    blacklist = db.token_blacklist
    token = event['authorizationToken']
    methodArn = event['methodArn']
    print(blacklist.find_one({'token': token}))
    if (token is None):
        return {'principalId': 'unauthorized', 'policyDocument': generatePolicy('Deny', methodArn)}
    elif ("Bearer " not in token):
        return {'principalId': 'unauthorized', 'policyDocument': generatePolicy('Deny', methodArn)}
    elif (blacklist.find_one({'token': token})):
        return {'principalId': 'unauthorized', 'policyDocument': generatePolicy('Deny', methodArn)}
    token = token.replace("Bearer ", "")
    try:
        decoded = jwt.decode(token, secret, algorithms=["HS256"])
        if ('_id' in decoded):
            userId = decoded['_id']
            policyDocument = generatePolicy('Allow', methodArn)
        else:
            userId = 'unauthorized'
            policyDocument = generatePolicy('Deny', methodArn)
    except jwt.ExpiredSignatureError:
        userId = 'unauthorized'
        policyDocument = generatePolicy('Deny', methodArn)
    return {'principalId': userId, 'policyDocument': policyDocument}

def generatePolicy(effect, methodArn):
    return{
        'Version': '2012-10-17',
        'Statement': [
          {
            'Action': "execute-api:Invoke",
            'Effect': effect,
            'Resource': methodArn
          }
        ]
    }