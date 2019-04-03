from flask import jsonify, make_response
import json

def response(message = None, content = None, status = 200):
    return {
        'statusCode': status,
        'body': json.dumps({
            'message': message,
            'content': content
        })
    }

def flaskResponse(message = None, content = None, status = 200):
    return make_response(jsonify({
        'message': message,
        'content': content
    }), status)
