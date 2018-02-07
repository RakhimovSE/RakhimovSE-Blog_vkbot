import vkapi
import command_system


def hello(data):
    first_name, last_name = vkapi.get_user_name(data['user_id'])
    message = 'Привет, %s %s!\nЯ - личный помощник Севастьяна Рахимова. Ты можешь задать интересующий тебя вопрос, ' \
              'а я передам его Севастьяну 😊' % (first_name, last_name)
    return message, ''


hello_command = command_system.Command()

hello_command.keys = ['привет', 'hello', 'hi', 'yo', 'wazzup', 'шалом', 'дратути', 'здравствуй', 'здравствуйте']
hello_command.description = 'Поприветствую тебя'
hello_command.process = hello
