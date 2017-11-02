import vk
from configparser import ConfigParser

cfg = ConfigParser()
cfg.read('config.ini')

token = cfg.get('BOT', 'token')
secret = cfg.get('BOT', 'secret')
confirmation_token = cfg.get('BOT', 'confirmation')

session = vk.Session()
api = vk.API(session, v=5.0)


def send_message(user_id, message, attachment):
    api.messages.send(access_token=token, user_id=user_id, message=message, attachment=attachment)
