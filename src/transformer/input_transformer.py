import json

def normalize(event):
    data = json.loads(event['body'])
    return [
        data['source'],
        data['url'],
        data['target_url']
    ]

def normalizeFlask(data):
    return [
        data['source'],
        data['url'],
        data['target_url']
    ]