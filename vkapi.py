import vk
import os
from configparser import ConfigParser

BOT_DIR = os.path.dirname(os.path.realpath(__file__))

cfg = ConfigParser()
cfg.read(BOT_DIR + '/config.ini')

token = cfg.get('BOT', 'token')
secret = cfg.get('BOT', 'secret')
confirmation = cfg.get('BOT', 'confirmation')

session = vk.Session()
api = vk.API(session, v=5.0)


def send_message(user_id, message, attachment):
    api.messages.send(access_token=token, user_id=user_id, message=message, attachment=attachment)


def get_user_name(user_id):
    data = api.users.get(user_ids=user_id)
    if 'response' not in data:
        return '', ''
    user = data['response'][0]
    return user['first_name'], user['last_name']
