import telebot
from random import randint
import sqlite3
import random

state=0

z=0

t=0
x1=0
x2=0


def get_state():
    return state


bot = telebot.TeleBot('')

connection = sqlite3.connect('info.db')
cursor = connection.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS users(
    userChatId INT PRIMARY KEY);
    """)

connection.commit()

@bot.message_handler(commands=['start'])
def send_description(message):
    bot.send_message(message.chat.id, 'Это бот-тренажер для решения различных задач,чтобы узнать функции бота введите '
                                      '/help')


@bot.message_handler(commands=['help'])
def send_description(message):
    bot.send_message(message.chat.id, '/math- открывает задания по математике')


@bot.message_handler(commands=['math'])
def send_description(message):
    bot.send_message(message.chat.id, 'Хотите решить квадратное уравнение')
    global state
    state = 1

@bot.message_handler(func=lambda message: get_state() == 1)
def givesq(message):
    n = -10
    m = 11
    global z
    z = random.randrange(n, m, 1)
    global t
    t = random.randrange(n, m, 1)
    if z+t>0 and z*t>0:
      bot.send_message(message.chat.id, f'x^2-{z+t}x+{z*t}=0')
      bot.send_message(message.chat.id, 'Введите ответ')
    elif z+t<0 and z*t>0:
        bot.send_message(message.chat.id, f'x^2+{-z -t}x+{z * t}=0')
        bot.send_message(message.chat.id, 'Введите ответ')
    elif z+t<0 and z*t<0:
        bot.send_message(message.chat.id, f'x^2+{-z - t}x{z * t}=0')
        bot.send_message(message.chat.id, 'Введите ответ')
    elif z+t>0 and z*t<0:
        bot.send_message(message.chat.id, f'x^2-{z + t}x{z * t}=0')
        bot.send_message(message.chat.id, 'Введите ответ')


    global state
    state = 2

@bot.message_handler(func=lambda message: get_state() == 2)
def otvet1(message):

    global x1
    x1=int(message.text)



    global state
    state = 3


@bot.message_handler(func=lambda message: get_state() == 3)
def otvet2(message):
    global x2

    x2 = int(message.text)
    if (x1==z and x2==t) or (x1==t and x2==z):
        bot.send_message(message.chat.id, 'Ответ верный')
    else:
        bot.send_message(message.chat.id, 'Ответ неверный')
        bot.send_message(message.chat.id, f'Верные ответы{z}  {t}')



    global state
    state = 4






@bot.message_handler(commands=['physical'])
def send_description(message):
    bot.send_message(message.chat.id, 'тест по физика')


@bot.message_handler(commands=['ruslang'])
def send_description(message):
    bot.send_message(message.chat.id, 'тест по тест по русскому языку')

@bot.message_handler(commands=['subscribe'])
def subscribe(message):
    # message.chat.id -> bd
    try:
        local_connection = sqlite3.connect('users.db')
        local_cursor = local_connection.cursor()
        local_cursor.execute("INSERT INTO users VALUES(?);", (message.chat.id,))
        local_connection.commit()
        bot.send_message(message.chat.id, "you have subscribed!")
    except Exception:
        bot.send_message(message.chat.id, "you have subscribed earlier")
    finally:
        print("happens after all")

@bot.message_handler(commands=['get_subscribers'])
def get_subscribers(message):
    local_connection = sqlite3.connect('info.db')
    local_cursor = local_connection.cursor()
    local_cursor.execute("SELECT * from users;")
    all_results = local_cursor.fetchall()

    bot.send_message(message.chat.id, str(all_results))


@bot.message_handler(content_types=['text'])
def send_description(message):
    if message!='/help' or message!='/math' or message!='/ruslang' or message!='/physical'or message!='/subscribe' or message!='/get_subscribers':
        bot.send_message(message.chat.id, 'Данной функции не существует')



bot.polling(none_stop=True, interval=0)
