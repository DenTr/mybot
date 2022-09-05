# Импортируем нужные компоненты
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import settings

logging.basicConfig(filename='bot.log', level=logging.INFO)

def greet_user(update, context):
    print('Вызван /start')
    update.message.reply_text('Привет, пользователь! Ты вызвал команду /start')

# Напишем функцию talk_to_me, которая будет "отвечать" пользователю
def talk_to_me(update, context):
    user_text = update.message.text 
    print(user_text)
    update.message.reply_text(user_text)

# Функция, которая соединяется с платформой Telegram, "тело" нашего бота
def main():
    # Создаем бота и передаем ему ключ для авторизации на серверах Telegram
    mybot = Updater(settings.API_KEY, use_context=True)
    
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    
    # укажем, что мы хотим реагировать только на текстовые сообщения - Filters.text
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    # залогируем в файл информацию о старте бота
    logging.info("Бот стартовал")

    # Командуем боту начать ходить в Telegram за сообщениями
    mybot.start_polling()
    # Запускаем бота, он будет работать, пока мы его не остановим принудительно
    mybot.idle()

# Вызываем функцию main() - именно эта строчка запускает бота
if __name__ == "__main__":
    main()