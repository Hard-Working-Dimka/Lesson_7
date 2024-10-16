import ptbot
import os
from dotenv import load_dotenv
from pytimeparse import parse

load_dotenv()
# TODO: ПРОВЕРИТЬ PEP8 ПО ДЕВМАНУ + IF NAME == MAIN


TG_TOKEN = os.getenv('TELEGRAM_TOKEN')  # подставьте свой ключ API


def render_progressbar(total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def notification_to_user(secs_left, user_id, message_id, message):
    progressbar_message = render_progressbar(parse(message), parse(message) - secs_left)
    bot.update_message(user_id, message_id, 'Осталось {0} секунд \n{1}'.format(secs_left, progressbar_message))


def run_out(user_id):
    bot.send_message(user_id, 'Время вышло!')


def start(user_id, message):
    message_id = bot.send_message(user_id, 'Запускаю таймер!')
    bot.create_countdown(parse(message), notification_to_user, user_id=user_id, message_id=message_id, message=message)
    bot.create_timer(parse(message), run_out, user_id=user_id)


load_dotenv()
bot = ptbot.Bot(TG_TOKEN)
bot.reply_on_message(start)
bot.run_bot()
