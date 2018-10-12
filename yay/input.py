from yay import core
from yay.util import *
from PyInquirer import prompt

def ask_user(data, variables):
    answers = prompt([data])
    variables.update(answers)


# Register tasks
core.register('User Input', ask_user)