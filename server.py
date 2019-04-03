import os
from src.transformer.input_transformer import normalizeFlask
from flask import Flask, request
from src.utils.helpers import flaskResponse
from os.path import join, dirname
from dotenv import load_dotenv
from src.methods.crawler import crawl

# load env
load_dotenv(join(dirname(__file__), '.env'))

# initiate flask app
app = Flask(__name__)

@app.route("/", methods=['POST'])
def flask_handler():
    try:
        if request.headers.get('secret') != os.getenv('API_SECRET'):
            return flaskResponse('not authorized', status=401)


        # get request input
        [source, url, target_url] = normalizeFlask(request.get_json())

        # crawl target url
        crawl(source, url, target_url)

        return flaskResponse('crawl completed', {'new': 0, 'done': 1})
    except:
        return flaskResponse('an error occurred', status=500)

if __name__ == '__main__':
   app.run(port=os.getenv('APP_PORT'))