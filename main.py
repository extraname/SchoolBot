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
    try:
        msg = bot.reply_to(message, f'Hello {message.from_user.first_name} , '
                                    f'nice to meet you', reply_markup=markup)
        bot.register_next_step_handler(msg, process_step)
    except AttributeError:
        msg = bot.reply_to(message, f'Hello, nice to meet you',
                           reply_markup=markup)
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
    result = f"Hello , it is {school[0]['name']}, {school[0]['link']} " \
             f"- it is our website. Now we have {school[0]['students']} " \
             f" students and {school[0]['teachers']} teachers. We have " \
             f"{school[0]['subjects_count']} courses"
    bot.send_message(message.chat.id, str(result))


@bot.message_handler(commands=['Students', 'students'])
def students_markup(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    students = requests.get(f'http://127.0.0.1:5000/students').json()
    st = [f"{i['name']} : {i['id']} " for i in students]
    markup.add("Back")
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
    elif message.text == "Back":
        send_welcome(message)
    else:
        send_single_student(message)


def send_students(message):
    students = requests.get('http://127.0.0.1:5000/students').json()
    for s in students:
        result = f"Student {s['name']}. Trained in a {s['course'][1:-1]} " \
                 f"course. The teacher was {s['teacher'][1:-1]}." \
                 f" During the training acquired programming skills." \
                 f" According to the results of the control, " \
                 f"he received the following assessments" \
                 f" by modules :{s['grade'][1:-2]}. Communication with " \
                 f"student - email : {s['email']}"
        bot.send_message(message.chat.id, result)


def send_single_student(message):
    m = message.text.split(": ")
    try:
        student = requests.get(
            f'http://127.0.0.1:5000/students/{int(m[1])}').json()
        s = student
        result = f"Student {s['name']}. Trained in a {s['course'][1:-1]} " \
                 f"course. The teacher was {s['teacher'][1:-1]}." \
                 f" During the training acquired programming skills." \
                 f" According to the results of the control, " \
                 f"he received the following assessments" \
                 f" by modules :{s['grade'][1:-2]}. Communication with " \
                 f"student - email : {s['email']}"
        bot.send_message(message.chat.id, result)
    except IndexError:
        bot.send_message(message.chat.id, "Please enter valid information,"
                                          " if nothing happens after pressing"
                                          " the button, enter /start again")


@bot.message_handler(commands=['Teachers', 'teachers'])
def teachers_markup(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    teachers = requests.get(f'http://127.0.0.1:5000/teachers').json()
    tch = [f"{i['name']} : {i['id']} " for i in teachers]
    markup.add('Back')
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
    elif message.text == "Back":
        send_welcome(message)
    else:
        send_single_teacher(message)


def send_teachers(message):
    teachers = requests.get('http://127.0.0.1:5000/teachers').json()
    for t in teachers:
        result = f"Teacher {t['name']}. The teacher of the {t['course']}" \
                 f" course. Email - {t['email']}"
        bot.send_message(message.chat.id, result)


def send_single_teacher(message):
    m = message.text.split(": ")
    try:
        teacher = requests.get(f'http://127.0.0.1:5000/teachers/{m[1]}').json()
        t = teacher
        result = f"Teacher {t['name']}. The teacher of the {t['course']}" \
                 f" course. Email - {t['email']}"
        # for k, v in teacher.items():
        bot.send_message(message.chat.id, result)

    except IndexError:
        bot.send_message(message.chat.id, "Please enter valid information,"
                                          " if nothing happens after pressing"
                                          " the button, enter /start again")


@bot.message_handler(commands=['Courses', 'courses'])
def courses_markup(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    courses = requests.get(f'http://127.0.0.1:5000/courses').json()
    cr = [f"{i['name']} : {i['id']} " for i in courses]
    markup.add("Back")
    markup.add("All")
    for i in cr:
        markup.add(str(i))
    msg = bot.reply_to(message, 'Hello. This is courses block, '
                                'click on the button to get information',
                       reply_markup=markup)
    bot.register_next_step_handler(msg, course_step)


def course_step(message):
    if message.text == 'All':
        send_courses(message)
    elif message.text == "Back":
        send_welcome(message)
    else:
        send_single_course(message)


def send_courses(message):
    courses = requests.get('http://127.0.0.1:5000/courses').json()
    for c in courses:
        result = f"Course {c['name']} consists of modules : " \
                 f"{c['modules'][1:-1]}. Course teacher - {c['teacher']}"
        bot.send_message(message.chat.id, result)


def send_single_course(message):
    m = message.text.split(": ")
    try:
        course = requests.get(f'http://127.0.0.1:5000/courses/{m[1]}').json()
        c = course
        result = f"Course {c['name']} consists of modules : " \
                 f"{c['modules'][1:-1]}. Course teacher - {c['teacher']}"
        bot.send_message(message.chat.id, result)
    except IndexError:
        bot.send_message(message.chat.id, "Please enter valid information,"
                                          " if nothing happens after pressing"
                                          " the button, enter /start again")


@bot.message_handler(commands=['Modules', 'modules'])
def modules_markup(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    modules = requests.get(f'http://127.0.0.1:5000/modules').json()
    mod = [f"{i['name']} : {i['id']} " for i in modules]
    markup.add("Back")
    markup.add("All")
    for i in mod:
        markup.add(str(i))
    msg = bot.reply_to(message, 'Hello. This is modules block, '
                                'click on the button to get information',
                       reply_markup=markup)
    bot.register_next_step_handler(msg, module_step)


def module_step(message):
    if message.text == 'All':
        send_modules(message)
    elif message.text == "Back":
        send_welcome(message)
    else:
        send_single_module(message)


def send_modules(message):
    modules = requests.get('http://127.0.0.1:5000/modules').json()
    for m in modules:
        result = f"The {m['name']} module is part of the course {m['course']}"
        bot.send_message(message.chat.id, result)


def send_single_module(message):
    m = message.text.split(": ")
    try:
        module = requests.get(f'http://127.0.0.1:5000/modules/{m[1]}').json()
        m = module
        result = f"The {m['name']} module is part of the course {m['course']}"
        bot.send_message(message.chat.id, result)
    except IndexError:
        bot.send_message(message.chat.id, "Please enter valid information,"
                                          " if nothing happens after pressing"
                                          " the button, enter /start again")


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'school':
        send_school(message)
    elif message.text.lower() == 'courses':
        courses_markup(message)
    elif message.text.lower() == 'teachers':
        teachers_markup(message)
    elif message.text.lower() == 'students':
        students_markup(message)
    elif message.text.lower() == 'modules':
        modules_markup(message)
    elif message.text.lower() == 'start':
        send_welcome(message)
    elif message.text.lower() == 'help':
        send_help(message)


if __name__ == "__main__":
    bot.polling()
