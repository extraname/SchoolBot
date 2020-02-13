import config
import requests
import telebot
from telebot import types

"""
This is a bot that receives information from REST API at localhost
"""

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=["help"])
def send_help(message):
    bot.send_message(message.chat.id,
                     "Hello ! It is project with name SchoolBot. "
                     "List of available commands: /start, /school, "
                     "/teachers, /courses, /modules, /students "
                     "You can receive information, but you cannot make changes"
                     )


"""
This function creates a menu with the possibility to follow buttons
"""


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('School', "Teachers", 'Courses', "Modules", "Students")
    msg = bot.reply_to(message, 'Hello, nice to meet you', reply_markup=markup)
    bot.register_next_step_handler(msg, process_step)


def process_step(message):
    if message.text == 'School':
        send_school(message)
    elif message.text == 'Teachers':
        teachers_markup(message)
    elif message.text == "Courses":
        courses_markup(message)
    elif message.text == "Students":
        students_markup(message)
    elif message.text == "Modules":
        modules_markup(message)


@bot.message_handler(commands=['School', 'school'])
def send_school(message):
    school = requests.get('http://127.0.0.1:5000/school').json()
    for k, v in school[0].items():
        s = f"{k} : {v}"
        bot.send_message(message.chat.id, str(s))


@bot.message_handler(commands=['Students', 'students'])
def students_markup(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    students = requests.get(f'http://127.0.0.1:5000/students').json()
    st = [f"Student : {i['id']} " for i in students]
    markup.add("All")
    for i in st:
        markup.add(str(i))
    msg = bot.reply_to(message,
                       'Hello. This is students block, '
                       'click on the button to get information',
                       reply_markup=markup)
    bot.register_next_step_handler(msg, st_step)


def st_step(message):
    if message.text == 'All':
        send_students(message)
    else:
        send_single_student(message)


def send_students(message):
    students = requests.get('http://127.0.0.1:5000/students').json()
    for i in students:
        bot.send_message(message.chat.id, str(i))


def send_single_student(message):
    m = message.text.split(": ")
    try:
        student = requests.get(
            f'http://127.0.0.1:5000/students/{int(m[1])}').json()
        for k, v in student.items():
            bot.send_message(message.chat.id, f"{k} : {v}")
    except IndexError:
        bot.send_message(message.chat.id, "Please enter valid information,"
                                          " if nothing happens after pressing"
                                          " the button, enter /start again")


@bot.message_handler(commands=['Teachers', 'teachers'])
def teachers_markup(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    teachers = requests.get(f'http://127.0.0.1:5000/teachers').json()
    tch = [f"Teacher : {i['id']} " for i in teachers]
    markup.add("All")
    for i in tch:
        markup.add(str(i))
    msg = bot.reply_to(message,
                       'Hello. This is teachers block,'
                       ' click on the button to get information',
                       reply_markup=markup)
    bot.register_next_step_handler(msg, teach_step)


def teach_step(message):
    if message.text == 'All':
        send_teachers(message)
    else:
        send_single_teacher(message)


def send_teachers(message):
    teachers = requests.get('http://127.0.0.1:5000/teachers').json()
    for i in teachers:
        bot.send_message(message.chat.id, str(i))


def send_single_teacher(message):
    m = message.text.split(": ")
    try:
        teacher = requests.get(f'http://127.0.0.1:5000/teachers/{m[1]}').json()
        for k, v in teacher.items():
            bot.send_message(message.chat.id, f"{k} : {v}")

    except IndexError:
        bot.send_message(message.chat.id, "Please enter valid information,"
                                          " if nothing happens after pressing"
                                          " the button, enter /start again")


@bot.message_handler(commands=['Courses', 'courses'])
def courses_markup(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    courses = requests.get(f'http://127.0.0.1:5000/courses').json()
    cr = [f"Course : {i['id']} " for i in courses]
    markup.add("All")
    for i in cr:
        markup.add(str(i))
    msg = bot.reply_to(message, 'Hello. This is students block, '
                                'click on the button to get information',
                       reply_markup=markup)
    bot.register_next_step_handler(msg, course_step)


def course_step(message):
    if message.text == 'All':
        send_courses(message)
    else:
        send_single_course(message)


def send_courses(message):
    courses = requests.get('http://127.0.0.1:5000/courses').json()
    for i in courses:
        bot.send_message(message.chat.id, str(i))


def send_single_course(message):
    m = message.text.split(": ")
    try:
        course = requests.get(f'http://127.0.0.1:5000/courses/{m[1]}').json()
        for k, v in course.items():
            bot.send_message(message.chat.id, f"{k} : {v}")
    except IndexError:
        bot.send_message(message.chat.id, "Please enter valid information,"
                                          " if nothing happens after pressing"
                                          " the button, enter /start again")


@bot.message_handler(commands=['Modules', 'modules'])
def modules_markup(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    modules = requests.get(f'http://127.0.0.1:5000/modules').json()
    mod = [f"Module : {i['id']} " for i in modules]
    markup.add("All")
    for i in mod:
        markup.add(str(i))
    msg = bot.reply_to(message, 'Hello. This is students block, '
                                'click on the button to get information',
                       reply_markup=markup)
    bot.register_next_step_handler(msg, module_step)


def module_step(message):
    if message.text == 'All':
        send_modules(message)
    else:
        send_single_module(message)


def send_modules(message):
    modules = requests.get('http://127.0.0.1:5000/modules').json()
    for i in modules:
        bot.send_message(message.chat.id, str(i))


def send_single_module(message):
    m = message.text.split(": ")
    try:
        course = requests.get(f'http://127.0.0.1:5000/modules/{m[1]}').json()
        for k, v in course.items():
            bot.send_message(message.chat.id, f"{k} : {v}")
    except IndexError:
        bot.send_message(message.chat.id, "Please enter valid information,"
                                          " if nothing happens after pressing"
                                          " the button, enter /start again")


if __name__ == "__main__":
    bot.polling()
