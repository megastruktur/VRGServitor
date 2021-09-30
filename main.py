from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import logging
from datetime import datetime, time
import pytz
import worker_parser
from dotenv import load_dotenv
import os

load_dotenv()

bot_token = os.environ.get('BOT_TOKEN')
updater = Updater(token=bot_token, use_context=True)
dispatcher = updater.dispatcher
group_chat_id = os.environ.get('GROUP_CHAT_ID')
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')


def start(update, context):
    print(update.effective_chat.id)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Приветствую. Меня зовут J.A.R.V.I.S. и я буду "
                                                                    "вашим ассистентом.")


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Прошу прощения, я не совсем Вас понимаю")


# Report reminder
def vrg_report_reminder_schedule():
    j = updater.job_queue
    t = time(hour=23, minute=00, second=00, tzinfo=pytz.timezone('Europe/Minsk'))
    j.run_daily(vrg_report_reminder_send, days=(0, 1, 2, 3, 4, 5, 6), time=t)


def vrg_report_reminder_send(context: CallbackContext):

    text = ''
    for worker in worker_parser.sheet_get_workers():
        text += worker_parser.workers[worker] + ' '
    text += ' Прошу прощения за беспокойство, напоминаю про необходимость написания отчёта.'
    context.bot.send_message(chat_id=group_chat_id, text=text)


def work_today(update, context):
    print(update.effective_chat.id)
    from_user = update.message.from_user
    text_confirm = '@' + from_user['username'] + ' Одну минуточку, произвожу сверку с расписанием.'
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_confirm)
    text = '@' + from_user['username'] + ' ' + ' и '.join(worker_parser.sheet_get_workers())
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def main():

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    # Start command handler call
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    # Who works today
    work_today_handler = CommandHandler('workToday', work_today)
    dispatcher.add_handler(work_today_handler)

    # Unknown Command
    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)

    # Reminder
    vrg_report_reminder_schedule()

    # Start Polling the API
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
