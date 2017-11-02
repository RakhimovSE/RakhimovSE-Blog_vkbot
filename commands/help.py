import command_system


def help(data):
    message = ''
    for c in command_system.command_list:
        message += c.keys[0] + ' - ' + c.description + '\n'
    return message, ''


help_command = command_system.Command()

help_command.keys = ['помощь', 'помоги', 'справка', 'help']
help_command.description = 'Покажу список команд'
help_command.process = help
