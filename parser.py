import glob
import json
import os
import requests
import re
import time
from datetime import datetime, timedelta
import random

def write_log_file(log_file_path, text):
    full_file_name = log_file_path + time.strftime("_%d.%m.%Y")
    with open(file=full_file_name, mode='a') as file:
        time_now = time.strftime("%d.%m.%Y %H:%M:%S")
        res_test = time_now + ' ' + text + '\n'
        file.write(res_test)

def del_log_file():
    del_day = (datetime.now() - timedelta(days=5)).strftime("%d.%m")
    del_log_file_name = glob.glob("./log/*"+del_day+"*")
    try:
        for file in del_log_file_name:
            os.remove(file)
    except Exception as ex:
        print(ex)


def get_data(url, get_html_log_path):
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        with open(file='index.html', mode='w') as file:
            file.write(response.text)
        write_log_file(get_html_log_path, "Get html is Success!")
    else:
        write_log_file(get_html_log_path, "Get html is Error!")

def get_parsing_dict(src):
    data = re.findall(r"class=\"section section-content section-bottom-collapse\"([^&]*?)</section>", src)
    today_info = data[0].split('weathertab weathertab')[2]
    now_info = data[0].split('weathertab weathertab')[1]
    info = {'today_precipitation': 'На улице вроде ничего',
            'today_precipitation_mm': '0',
            'today_min_temp': '0',
            'today_max_temp': '0',
            'now_precipitation': 'Не выходи из комнаты',
            'now_temperature': '0',
            'feel_temperature': '0'}
    info['today_day'] = time.strftime("%a %d %b", time.localtime())
    info['time'] = time.strftime("%H:%M", time.localtime())
    re_samples = {'today_day': r"<div class=\"date [^>]*?\">([^>]*?)</div>",
                  'today_precipitation': r"data-text=\"([^>]*?)\">",
                  'today_precipitation_mm': r"<div class=\"precipitation\">([^<]*?)</div>",
                  'today_min_temp': r"class=\"unit unit_temperature_c\">([^>]*?)</span>",
                  'today_max_temp': r"class=\"unit unit_temperature_c\">([^>]*?)</span>",
                  'now_precipitation': r"data-text=\"([^>]*?)\">",
                  'now_temperature': r"class=\"unit unit_temperature_c\"><span class=\"sign\">([^%]*?)<span",
                  'feel_temperature': r"class=\"unit unit_temperature_c\"><span class=\"sign\">([^%]*?)<span"}
    for key, value in re_samples.items():
        if (key[0] == 't'):
            x = re.findall(value, today_info)
        else:
            x = re.findall(value, now_info)
        if ((x and key != 'today_max_temp') and (x and key != 'feel_temperature')):
            info[key] = x[0]
        elif(x):
            info[key] = x[1]
    info['now_temperature'] = "".join(info['now_temperature'].split('</span>')).replace(" ","")
    info['feel_temperature'] = "".join(info['feel_temperature'].split('</span>')).replace(" ", "")
    write_log_file(parsing_log_path, "Parsing html is Success!")
    return info

def parsing(file_path, parsing_log_path):
    try:
        with open(file_path, encoding="utf-8") as file:
            src = file.read()
            info = get_parsing_dict(src)
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
    url = 'https://www.gismeteo.ru/weather-kazan-4364/now/'
    get_html_log_path = './log/get_html_log'
    parsing_log_path = './log/pars_log'    # get_data(url, get_html_log_path)

    while True:
        get_data(url, get_html_log_path)
        parsing(html_file_path, parsing_log_path)
        x = random.randint(0, 50)
        del_log_file()
        time.sleep(1200+x)