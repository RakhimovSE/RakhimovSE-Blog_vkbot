from flask import Flask, request, json
# from settings import *
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
        return messageHandler.vkapi.confirmation_token
    elif data['type'] == 'message_new':
        messageHandler.create_answer(data['object'])
    return 'ok'
