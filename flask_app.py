from flask import Flask, request, json
import messageHandler

app = Flask(__name__)


@app.route('/')
def main():
    return 'Hello from flask!'


@app.route('/', methods=['POST'])
def processing():
    data = json.loads(request.data)
    if 'type' not in data.keys():
        return 'not vk'
    if data['type'] == 'confirmation':
        return messageHandler.vkapi.confirmation
    if 'secret' in data and data['secret'] != messageHandler.vkapi.secret:
        return 'wrong secret code'
    if data['type'] == 'message_new':
        messageHandler.create_answer(data['object'])
    return 'ok'
