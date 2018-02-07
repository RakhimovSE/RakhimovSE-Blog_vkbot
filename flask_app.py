from flask import Flask, request, json
import messageHandler

app = Flask(__name__)


@app.route('/')
def main():
    return 'Hello from flask!'


@app.route('/user_name', methods=['GET'])
def user_name():
    user_id = int(request.args['user_id'])
    first_name, last_name = messageHandler.vkapi.get_user_name(user_id)
    return 'Name for %d is %s %s' % (user_id, first_name, last_name)


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
