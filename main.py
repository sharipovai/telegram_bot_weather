import json
from telebot import types
import telebot
import random
from datetime import datetime
import requests


def get_weather():
    api_key ='d1c9199f445904e20cb47035827588b8'
    latitude = 55.7887
    longitude = 49.1221
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}&units=metric&lang=ru"
    response = requests.get(url)
    weather_dict = response.json()
    now_weather_dict = {}
    now_weather_dict['feels_like'] = int(weather_dict['main']['feels_like'])
    now_weather_dict['temp'] = int(weather_dict['main']['temp'])
    now_weather_dict['temp_min'] = int(weather_dict['main']['temp_min'])
    now_weather_dict['temp_max'] = int(weather_dict['main']['temp_max'])
    now_weather_dict['description'] = weather_dict['weather'][0]['description']
    now_weather_dict['time'] = datetime.fromtimestamp(weather_dict['dt']).strftime("%d.%m.%Y %H:%M")
    if 'snow' in weather_dict.keys():
        now_weather_dict['snow'] = weather_dict['snow']['1h']
    if 'rain' in weather_dict.keys():
        now_weather_dict['rain'] = weather_dict['rain']['1h']
    return now_weather_dict


def write_motivation():
    with open("Мотивация.txt", "r", encoding="utf8") as file:
        mot_str = file.readline()
        mot_arr = mot_str.split("/ ")
        mot_arr = [line.rstrip()  for line in mot_arr if len(line) > 10]
        x = random.randint(0, len(mot_arr)-1)
        return mot_arr[x]

def write_weather():
    now_weather_dict = get_weather()
    answer = f"К {now_weather_dict['time']} в Казани\n{now_weather_dict['description']}\n"\
    f"{now_weather_dict['temp']} С. По ощущению {now_weather_dict['feels_like']} С."
    if 'snow' in now_weather_dict.keys():
        answer += f"Снег {now_weather_dict['snow']} мм\n"
    if 'rain' in now_weather_dict.keys():
        answer += f"Дождь {now_weather_dict['rain']} мм\n"
    return answer


bot = telebot.TeleBot('6624143242:AAGLlbJhfa-2KwEeLclcvxd82Rn0M0wpoPg')


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}!')
    wait_command(message)

def wait_command(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Погода')
    btn2 = types.KeyboardButton('Мотивация')
    markup.row(btn1, btn2)
    bot.send_message(message.chat.id, f'Тебе погоду или мотивацию?\n', reply_markup=markup)
    bot.register_next_step_handler(message, info)


@bot.message_handler(commands=["text"])
def info(message):
    if message.text.lower() == 'привет' or message.text.lower() == 'привет!':
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}!')
    elif 'погод' in message.text.lower():
        answer = write_weather()
        bot.send_message(message.chat.id, answer, parse_mode='html')
    elif 'мотивац' in message.text.lower():
        answer = write_motivation()
        bot.send_message(message.chat.id, answer, parse_mode='html')
    else:
        bot.send_message(message.chat.id, '<b>Я пока не знаю такой команды</b>', parse_mode='html')
    wait_command(message)


bot.infinity_polling()
