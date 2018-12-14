import json

def response(message = None, content = None, status = 200):
    return {
        'statusCode': status,
        'body': json.dumps({
            'message': message,
            'content': content
        })
    }