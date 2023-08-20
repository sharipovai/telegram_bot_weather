import json
import webbrowser
import telebot
def read_data_file():
    try:
        with open("results.json", "r", encoding="utf-8") as read_file:
            return json.load(read_file)
    except Exception as ex:
        return {}

bot = telebot.TeleBot('6624143242:AAGLlbJhfa-2KwEeLclcvxd82Rn0M0wpoPg')

@bot.message_handler(commands=['start', 'hello'])
def main(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}  {message.from_user.last_name}!')

@bot.message_handler(commands=['weather'])
def main(message):
    data = read_data_file()
    bot.send_message(message.chat.id, f"Сегодня в Казани {data['today_day']} {data['today_min_temp']} {data['today_max_temp']}")

@bot.message_handler(commands=['help'])
def main(message):
    bot.send_message(message.chat.id, '<b>Для получения прогноза погоды введите /weather </b>', parse_mode='html')

@bot.message_handler()
def info(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}  {message.from_user.last_name}!')
    elif message.text.lower() == 'id':
        bot.reply_to(message, f'ID: {message.from_user.id}')
    else:
        bot.send_message(message.chat.id, '<b>Я пока не знаю такой команды</b>', parse_mode='html')


bot.polling(none_stop=True)