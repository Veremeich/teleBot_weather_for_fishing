import schedule  # ежедневное выполнение
import time  # время
import requests  # доступ до сайта
from datetime import date  # дата
from bs4 import BeautifulSoup  # парсинг по сайту
from ast import literal_eval


today = date.today().strftime('%d.%m.%Y')

# сайт синоптик
r = requests.get('http://cgo-sreznevskyi.kyiv.ua/index.php?fn=k_meteo&f=kyiv')

html = BeautifulSoup(r.text, 'lxml')

parsing_str = html.select('tr')[6].text
table_list = parsing_str.split('\xa0')
table_list2 = table_list[:8]


db_weather = open("./test1/db_weather.txt", "r")
for line in db_weather:
    new = literal_eval(line)
w = list(new)


def upprnd_db_weather():

    w.insert(0, table_list2)
    f = open('db_weather.txt', 'w')
    f.write(str(w))
    f.close()
    return w


upprnd_db_weather()


def split_list(list, wanted_parts=60):
    length = len(list)
    return [list[i*length // wanted_parts: (i+1)*length // wanted_parts]
            for i in range(wanted_parts)]


schedule.every().day.at("10:00").do(upprnd_db_weather)

while True:
    schedule.run_pending()
    time.sleep(1)

