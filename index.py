

import json
from flask import Flask, request, jsonify
from data import Deployment


app = Flask(__name__)





@app.route('/')
def index():
    return json.dumps({'name': 'alice',
                       'email': 'alice@outlook.com'})


@app.route('/send', methods=['post'])
def process_request():
    data = request.json
    prossData = Deployment()
    fianldata = prossData.request(data)

    return jsonify(fianldata)








if __name__ == '__main__':
    app.run(debug=True)