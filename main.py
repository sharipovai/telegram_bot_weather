import json
from telebot import types
import telebot
def read_data_file():
    try:
        with open("results.json", "r", encoding="utf-8") as read_file:
            return json.load(read_file)
    except Exception as ex:
        return {}

bot = telebot.TeleBot('6624143242:AAGLlbJhfa-2KwEeLclcvxd82Rn0M0wpoPg')

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Погода')
    markup.row(btn1)
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}!', reply_markup=markup)
    bot.register_next_step_handler(message, on_click)

def on_click(message):
    if message.text == 'Погода':
        data = read_data_file()
        if (data['today_precipitation_mm'] != '0'):
            answer = f"Сегодня в Казани\n<b><u>{data['today_day']}</u></b> \n" \
                     f"{data['today_precipitation']} {data['today_precipitation_mm']}\n" \
                     f"{data['today_min_temp']} {data['today_max_temp']}"
        else:
            answer = f"Сегодня в Казани <b>{data['today_day']}</b> \n" \
                     f"{data['today_precipitation']} \n" \
                     f"{data['today_min_temp']} {data['today_max_temp']}"
        bot.send_message(message.chat.id, answer, parse_mode='html')

@bot.message_handler()
def info(message):
    if message.text.lower() == 'привет' or message.text.lower() == 'привет!':
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}!')
    elif message.text.lower() == 'погода':
        on_click(message)
    else:
        bot.send_message(message.chat.id, '<b>Я пока не знаю такой команды</b>', parse_mode='html')

bot.polling(none_stop=True)