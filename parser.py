import json
import requests
import re
import time
from datetime import date
import random

def write_log_file(log_file_path, text):
    with open(file=log_file_path, mode='a') as file:
        time_now = time.strftime("%d.%m.%Y %H:%M:%S")
        res_test = time_now + ' ' + text + '\n'
        file.write(res_test)

def get_data(url, get_html_log_path):
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        with open(file='index.html', mode='w') as file:
            file.write(response.text)
        write_log_file(get_html_log_path, "Get html is Success!")
    else:
        write_log_file(get_html_log_path, "Get html is Error!")

def parsing(file_path, parsing_log_path):
    try:
        with open(file_path, encoding="utf-8") as file:
            src = file.read()
            data = re.findall(r"class=\"section section-content section-bottom-collapse\"([^&]*?)</section>", src)
            today_info = data[0].split('weathertab weathertab')[1]
            info = {}
            info['today_day'] = re.findall(r"<div class=\"date [^>]*?\">([^>]*?)</div>", today_info)[0]
            info['today_min_temp'] = re.findall(r"class=\"unit unit_temperature_c\">([^>]*?)</span>", today_info)[0]
            info['today_max_temp'] = re.findall(r"class=\"unit unit_temperature_c\">([^>]*?)</span>", today_info)[1]
            info['time'] = str(date.today())
            # print(info)
            write_log_file(parsing_log_path, "Parsing html is Success!")
    except Exception as ex:
        write_log_file(parsing_log_path, "Parsing html is Error!")
    try:
        with open("results.json", "w", encoding="utf-8") as file:
            json.dump(info, file, indent=4, ensure_ascii=False)
        write_log_file(parsing_log_path, "Writing json is Success!")
    except Exception as ex:
        write_log_file(parsing_log_path, "Writing json is Error!")

if __name__ == '__main__':
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8'
    }
    html_file_path = './index.html'
    url = 'https://www.gismeteo.ru/weather-kazan-4364/tomorrow/'
    get_html_log_path = './log/get_html_log'
    parsing_log_path = './log/pars_log'    # get_data(url, get_html_log_path)

    while True:
        get_data(url, get_html_log_path)
        parsing(html_file_path, parsing_log_path)
        x = random.randint(0, 50)
        time.sleep(1800+x)