import vkapi
import os
import importlib
from command_system import command_list
import apiai, json


def load_modules():
    # путь от рабочей директории, ее можно изменить в настройках приложения
    files = os.listdir(vkapi.BOT_DIR + '/commands')
    modules = filter(lambda x: x.endswith('.py'), files)
    for m in modules:
        importlib.import_module("commands." + m[0:-3])


def get_answer(data):
    body = data['body'].lower()
    message = ''
    attachment = ''
    distance = len(body)
    command = None
    key = ''
    for c in command_list:
        for k in c.keys:
            d = damerau_levenshtein_distance(body, k)
            if d < distance:
                distance = d
                command = c
                key = k
                if distance == 0:
                    message, attachment = c.process(data)
                    return message, attachment
    if float(distance) < len(body) * 0.4:
        message, attachment = command.process(data)
        message = 'Я понял твой запрос как "%s"\n\n' % key + message
    return message, attachment


def get_dialogflow_text_message(data):
    body = data['body'].lower()
    request = apiai.ApiAI('a36518ee37714bcb8a98ebac6bfa6ad6').text_request()  # Токен API к Dialogflow
    request.lang = 'ru'  # На каком языке будет послан запрос
    request.session_id = 'BatlabAIBot'  # ID Сессии диалога (нужно, чтобы потом учить бота)
    request.query = body  # Посылаем запрос к ИИ с сообщением от юзера
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))
    response = responseJson['result']['fulfillment']['speech']  # Разбираем JSON и вытаскиваем ответ
    # Если есть ответ от бота - присылаем юзеру, если нет - бот его не понял
    return response if response else 'Я тебя не совсем понял! Напиши "помощь", чтобы узнать мои команды. ' \
                                     'Либо мы можем просто пообщаться 😊'


def create_answer(data):
    load_modules()
    user_id = data['user_id']
    message, attachment = get_answer(data)
    if not message:
        message = get_dialogflow_text_message(data)
    vkapi.send_message(user_id, message, attachment)


def damerau_levenshtein_distance(s1, s2):
    d = {}
    lenstr1 = len(s1)
    lenstr2 = len(s2)
    for i in range(-1, lenstr1 + 1):
        d[(i, -1)] = i + 1
    for j in range(-1, lenstr2 + 1):
        d[(-1, j)] = j + 1
    for i in range(lenstr1):
        for j in range(lenstr2):
            if s1[i] == s2[j]:
                cost = 0
            else:
                cost = 1
            d[(i, j)] = min(
                d[(i - 1, j)] + 1,  # deletion
                d[(i, j - 1)] + 1,  # insertion
                d[(i - 1, j - 1)] + cost,  # substitution
            )
            if i and j and s1[i] == s2[j - 1] and s1[i - 1] == s2[j]:
                d[(i, j)] = min(d[(i, j)], d[i - 2, j - 2] + cost)  # transposition
    return d[lenstr1 - 1, lenstr2 - 1]
