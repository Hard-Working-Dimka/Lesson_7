import ptbot
import os
from dotenv import load_dotenv
from pytimeparse import parse


def render_progressbar(total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def notifications_to_user(secs_left, user_id, message_id, total_tima):
    progressbar_message = render_progressbar(total_tima, total_tima - secs_left)
    bot.update_message(user_id, message_id, 'Осталось {0} секунд \n{1}'.format(secs_left, progressbar_message))


def timer_run_out(user_id):
    bot.send_message(user_id, 'Время вышло!')


def start(user_id, time_from_user):
    total_tima = parse(time_from_user)
    message_id = bot.send_message(user_id, 'Запускаю таймер!')
    bot.create_countdown(total_tima, notifications_to_user, user_id=user_id, message_id=message_id,
                         total_tima=total_tima)
    bot.create_timer(parse(time_from_user), timer_run_out, user_id=user_id)


def main():
    load_dotenv()
    global bot
    bot = ptbot.Bot(os.getenv('TELEGRAM_TOKEN'))
    bot.reply_on_message(start)
    bot.run_bot()


if __name__ == '__main__':
    main()
