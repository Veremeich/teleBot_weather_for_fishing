import matplotlib.pyplot as plt
from datetime import date, timedelta
import telebot
from telebot import types
import os
from ast import literal_eval
import requests
from bs4 import BeautifulSoup

today = date.today().strftime('%d.%m.%Y')
day7 = date.today() - timedelta(days=6)
day6 = date.today() - timedelta(days=5)
day5 = date.today() - timedelta(days=4)
day4 = date.today() - timedelta(days=3)
day3 = date.today() - timedelta(days=2)
day2 = date.today() - timedelta(days=1)


r = requests.get('http://cgo-sreznevskyi.kyiv.ua/index.php?fn=k_meteo&f=kyiv')

html = BeautifulSoup(r.text, 'lxml')

parsing_str = html.select('tr')[6].text
table_list = parsing_str.split('\xa0')
table_list2 = table_list[:8]


day_values = ('Дата: ' + table_list2[0] + '\n' + 'Температура повітря, oC: ' + table_list2[1] + '\n' + 'Вологість повітря, % : ' + table_list2[2] + '\n' + 'Напрям вітру: ' + table_list2[3] +
              '\n' + 'Максимальна швидкість вітру, м/с: ' + table_list2[4] + '\n' + 'Атмосферний тиск, гПа: ' + table_list2[5] + '\n' + 'Атмосферний тиск, мм рт.ст.: ' + table_list2[6])


db_weather = open("./db_weather.txt", "r")


for line in db_weather:
    new = literal_eval(line)


for row in new:
    for elem in row:

        if elem == day7.strftime('%d.%m.%Y'):
            data1 = row[0]
            temp1 = float(row[1])
            pressure1 = int(row[6])
            humidity1 = int(row[2])
            wind1 = row[3]
        if elem == day6.strftime('%d.%m.%Y'):

            data2 = row[0]
            temp2 = float(row[1])
            pressure2 = int(row[6])
            humidity2 = int(row[2])
            wind2 = row[3]
        if elem == day5.strftime('%d.%m.%Y'):
            data3 = row[0]
            temp3 = float(row[1])
            pressure3 = int(row[6])
            humidity3 = int(row[2])
            wind3 = row[3]
        if elem == day4.strftime('%d.%m.%Y'):
            data4 = row[0]
            temp4 = float(row[1])
            pressure4 = int(row[6])
            humidity4 = int(row[2])
            wind4 = row[3]
        if elem == day3.strftime('%d.%m.%Y'):
            data5 = row[0]
            temp5 = float(row[1])
            pressure5 = int(row[6])
            humidity5 = int(row[2])
            wind5 = row[3]
        if elem == day2.strftime('%d.%m.%Y'):
            data6 = row[0]
            temp6 = float(row[1])
            pressure6 = int(row[6])
            humidity6 = int(row[2])
            wind6 = row[3]
        if elem == today:
            data7 = row[0]
            temp7 = float(row[1])
            pressure7 = int(row[6])
            humidity7 = int(row[2])
            wind7 = row[3]

db_weather.close()


def press():

    fig, ax = plt.subplots()
    x = [data1, data2, data3, data4, data5, data6, data7]
    y = [pressure1, pressure2, pressure3,
         pressure4, pressure5, pressure6, pressure7]
    plt.plot(x, y)
    plt.scatter(x, y)
    ax.set_facecolor('seashell')
    fig.set_facecolor('floralwhite')
    fig.set_figwidth(12)
    fig.set_figheight(6)
    plt.title(r'Давление за прошедшую неделю')
    plt.ylabel(r'мм. рт.ст.')
    plt.xlabel(r'Дата')
    plt.grid(True)
    plt.savefig('pressure_figure.png')


press()


def humid():
    fig, ax = plt.subplots()
    x = [data1, data2, data3, data4, data5, data6, data7]
    y = [humidity1, humidity2, humidity3,
         humidity4, humidity5, humidity6, humidity7]
    plt.plot(x, y)
    plt.scatter(x, y)
    ax.set_facecolor('seashell')
    fig.set_facecolor('floralwhite')
    fig.set_figwidth(12)
    fig.set_figheight(6)
    plt.title(r'Влажность за прошедшую неделю')
    plt.ylabel(r'%')
    plt.xlabel(r'Дата')
    plt.grid(True)

    plt.savefig('humidity.png')


humid()


def temperature():
    fig, ax = plt.subplots()
    x = [data1, data2, data3, data4, data5, data6, data7]
    y = [temp1, temp2, temp3,
         temp4, temp5, temp6, temp7]
    plt.plot(x, y)
    plt.scatter(x, y)
    ax.set_facecolor('seashell')
    fig.set_facecolor('floralwhite')
    fig.set_figwidth(12)
    fig.set_figheight(6)
    plt.title(r'Температура за прошедшую неделю')
    plt.ylabel(r'oC')
    plt.xlabel(r'Дата')
    plt.grid(True)

    plt.savefig('Tempereture.png')


temperature()


bot = telebot.TeleBot('TOKEN')


@bot.message_handler(commands=["start"])
def start(m, res=False):
    # Добавляем две кнопки
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Давление")
    item2 = types.KeyboardButton("Ветер")
    item3 = types.KeyboardButton("Влажность")
    item4 = types.KeyboardButton("Температура")
    item5 = types.KeyboardButton("Выбрать дату")
    markup.add(item1)
    markup.add(item2)
    markup.add(item3)
    markup.add(item4)
    markup.add(item5)
    bot.send_message(
        m.chat.id, day_values,  reply_markup=markup)


@bot.message_handler(content_types=["text"])
def handle_text(message):
    # Если юзер прислал 1,
    if message.text.strip() == 'Давление':
        press()
        bot.send_photo(message.chat.id, open('./pressure_figure.png', 'rb'))
        plt.close()
        os.remove('./pressure_figure.png')
    # Если юзер прислал 2,
    elif message.text.strip() == 'Ветер':
        bot.send_message(
            message.chat.id, (f'{data1}: {wind1} \n{data2}: {wind2}\n{data3}: {wind3}\n{data4}: {wind4}\n{data5}: {wind5}\n{data6}: {wind6}\n{data7}: {wind7}\n'))
    # Если юзер прислал 3,
    elif message.text.strip() == 'Влажность':
        humid()
        bot.send_photo(message.chat.id, open('./humidity.png', 'rb'))
        plt.close()
        os.remove('./humidity.png')
    elif message.text.strip() == 'Температура':
        temperature()
        bot.send_photo(message.chat.id, open('./Tempereture.png', 'rb'))
        plt.close()
        os.remove('./Tempereture.png')
    # Отсылаем юзеру сообщение
    elif message.text.strip() == 'Выбрать дату':
        bot.send_message(
            message.chat.id, 'Архив данных ведется с 01.12.2021г!\nВы можете выбрать любую дату в формате день.месяц.год! Например: 20.03.2022!\nВыбранная дата будет последним днем недельного отрезка.\nВведите дату:')
        bot.register_next_step_handler(message, handle_text2)


@bot.message_handler(content_types=["text"])
def handle_text2(m):
    try:

        for row in new:
            for elem in row:
                if m.text.strip() == elem:
                    slice_ = new[(new.index(row)):(new.index(row))+7]

                    pressure_slice = [int(slice_[6][6]), int(slice_[5][6]), int(slice_[4][6]), int(
                        slice_[3][6]), int(slice_[2][6]), int(slice_[1][6]), int(slice_[0][6])]

                    humidity_slice = [int(slice_[6][2]), int(slice_[5][2]), int(slice_[4][2]), int(
                        slice_[3][2]), int(slice_[2][2]), int(slice_[1][2]), int(slice_[0][2])]

                    wind_slice = str(
                        f'{slice_[6][0]}: {slice_[6][3]}\n{slice_[5][0]}: {slice_[5][3]}\n{slice_[4][0]}: {slice_[4][3]}\n{slice_[3][0]}: {slice_[3][3]}\n{slice_[2][0]}: {slice_[2][3]}\n{slice_[1][0]}: {slice_[1][3]}\n{slice_[0][0]}: {slice_[0][3]} \n')

        fig, ax = plt.subplots()
        x = [slice_[6][0], slice_[5][0], slice_[4][0], slice_[
            3][0], slice_[2][0], slice_[1][0], slice_[0][0]]
        y = pressure_slice
        plt.plot(x, y)
        plt.scatter(x, y)
        ax.set_facecolor('seashell')
        fig.set_facecolor('floralwhite')
        fig.set_figwidth(12)
        fig.set_figheight(6)
        plt.title(r'Давление')
        plt.ylabel(r'мм. рт.ст.')
        plt.xlabel(r'Дата')
        plt.grid(True)
        plt.savefig('pressure_figure.png')
        bot.send_photo(m.chat.id, open(
            './pressure_figure.png', 'rb'))
        plt.close()
        os.remove('./pressure_figure.png')

        bot.send_message(
            m.chat.id, wind_slice)

        fig, ax = plt.subplots()
        x = [slice_[6][0], slice_[5][0], slice_[4][0], slice_[
            3][0], slice_[2][0], slice_[1][0], slice_[0][0]]
        y = humidity_slice
        plt.plot(x, y)
        plt.scatter(x, y)
        ax.set_facecolor('seashell')
        fig.set_facecolor('floralwhite')
        fig.set_figwidth(12)
        fig.set_figheight(6)
        plt.title(r'Влажность')
        plt.ylabel(r'%')
        plt.xlabel(r'Дата')
        plt.grid(True)
        plt.savefig('humidity.png')
        bot.send_photo(m.chat.id, open('./humidity.png', 'rb'))
        plt.close()
        os.remove('./humidity.png')
    except Exception:
        bot.send_message(
            m.chat.id, 'Такой даты нет. нажмите кнопку "Выбор даты" и повторите ввод даты')

    # Запускаем бота
bot.polling(none_stop=True, interval=0)
