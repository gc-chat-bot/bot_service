from flask import request, json, Response, Flask
from infopuls_crawler.service import handlers, UserRequest

app = Flask(__name__)

handlers = handlers()


@app.route('/handle', methods=['POST'])
def serve():
    request_json = request.json
    text = request_json["text"]
    chat_id = request_json["chat_id"]
    session_id = 123  # request_json["session_id"]

    user_request = UserRequest(chat_id, session_id, text)
    user_response = handlers.process_request(user_request)
    print(user_response.text)

    data = {
        "text": user_response.text,
        'chat_id': chat_id,
        'session_id': session_id
    }
    js = json.dumps(data)

    resp = Response(js, status=200, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3001)
