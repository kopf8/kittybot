import logging
import os
import requests

from datetime import datetime
from dotenv import load_dotenv
from random import randint
from telebot import TeleBot, types

load_dotenv()
secret_token = os.getenv('TOKEN')
bot = TeleBot(token=secret_token)
URL = 'https://api.thecatapi.com/v1/images/search'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)


def get_new_image():
    try:
        response = requests.get(URL)
    except Exception as error:
        logging.error(f'An error occured when trying to contact the main API '
                      f'server: {error}')
        new_url = 'https://api.thedogapi.com/v1/images/search'
        response = requests.get(new_url)
    response = response.json()
    random_cat = response[0].get('url')
    return random_cat


def get_ip_details_str(ip_address):
    ip_token = os.getenv('IP_TOKEN')
    details = requests.get(url=f'http://ipinfo.io/{ip_address}/?'
                               f'token={ip_token}')
    if details.status_code == 200:
        details = details.json()
        formatted_details = f'{"-"*30}\nIP Details\n{"-"*30}\n'
        for key in details:
            formatted_details += f'{key} : {details[key]}\n'
    elif details.status_code == 404:
        formatted_details = "IP you've entered is invalid."
    return formatted_details


@bot.message_handler(commands=['newcat'])
def new_cat(message):
    chat = message.chat
    bot.send_photo(chat.id, get_new_image())


@bot.message_handler(commands=['ip'])
def show_ip(message):
    
    ip_address = message.text.split('/ip')[-1].strip()
    details = get_ip_details_str(ip_address)
    bot.reply_to(message=message, text=details)


@bot.message_handler(commands=['time'])
def show_time(message):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    chat = message.chat
    chat_id = chat.id
    bot.send_message(
        chat_id=chat_id,
        text='Current time is: {}'.format(current_time)
    )


@bot.message_handler(commands=['random_digit'])
def get_random_digit(message):
    random_digit = randint(1, 10)
    chat = message.chat
    chat_id = chat.id
    bot.send_message(chat_id=chat_id, text=str(random_digit))


@bot.message_handler(commands=['start'])
def wake_up(message):
    chat = message.chat
    name = message.chat.first_name
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard.row(
        types.KeyboardButton('/newcat'),
        types.KeyboardButton('/time'),
    )
    keyboard.row(
        types.KeyboardButton('/ip'),
        types.KeyboardButton('/random_digit'),
    )

    bot.send_message(
        chat_id=chat.id,
        text=f'Hello, {name}, look at this cute cat!',
        reply_markup=keyboard,
    )

    bot.send_photo(chat.id, get_new_image())


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "Sorry, this command is not supported yet.")


def main():
    print('[*] Starting Bot...')
    bot.polling()
    print('[!] Bot Stopped...')


if __name__ == '__main__':
    main()
