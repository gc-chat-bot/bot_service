from flask import request, json, Response, Flask

app = Flask(__name__)


@app.route('/handle', methods=['POST'])
def serve():
    request_json = request.json
    text = request_json["text"]
    chat_id = request_json["chat_id"]
    data = {
        "text": text,
        'chat_id': chat_id
    }
    js = json.dumps(data)

    resp = Response(js, status=200, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3001)
