"""
Домашнее задание №1

Использование библиотек: ephem

* Установите модуль ephem
* Добавьте в бота команду /planet, которая будет принимать на вход
  название планеты на английском, например /planet Mars
* В функции-обработчике команды из update.message.text получите
  название планеты (подсказка: используйте .split())
* При помощи условного оператора if и ephem.constellation научите
  бота отвечать, в каком созвездии сегодня находится планета.

"""

# Импортируем нужные компоненты
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import settings
import ephem

# Теперь, настроим логирование. Будем записывать все сообщения уровня INFO и выше в файл bot.log.
logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log')

# создадим список планет из ephem
list_planets = []
for planet in range(8):
  list_planets.append(ephem._libastro.builtin_planets()[planet][2].lower())

def greet_user(update, context): #  вопрос - зачем нужен аргумент context?
    text = 'Привет, пользователь!'
    print(text) # эта строка распечатывает текст внутри терминала
    update.message.reply_text(text) # эта строка передает информацию от бота пользователю внутри телеграмма

# создаем функция для определения созвездия
def constellation_search(update, planet_name):
  planet = getattr(ephem, planet_name.capitalize())()
  update.message.reply_text(str(ephem.constellation(planet)))

Зачем мы обращаемся к getattr?
  
# Напишем функцию planet_name, которая будет получать от пользователя название планеты
def get_planet_name(update, context):
    text = 'Вызван /planet'
    print(text)
    update.message.reply_text('Введите название планеты')  # сообщение от бота внутри телеграмма
    planet_name = update.message.text.lower() # это передача инормации от пользователя в телеграмм
    
    if planet_name not in list_planets:
      update.message.reply_text('Вы точно ввели имя планеты?')
      update.message.reply_text('Надо ввести имя планеты из Солнечной системы')
    else:
      update.message.reply_text(constellation_search(update, planet_name))
 
# Функция, которая соединяется с платформой Telegram, "тело" нашего бота
def main():
    # Создаем бота и передаем ему ключ для авторизации на серверах Telegram
    mybot = Updater(settings.API_KEY, use_context=True)
    
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    
    # укажем, что мы хотим реагировать только на текстовые сообщения - Filters.text
    # dp.add_handler(MessageHandler(Filters.text, planet_name))
    dp.add_handler(CommandHandler("planet", get_planet_name))

    # залогируем в файл информацию о старте бота
    logging.info("Бот стартовал")

    # Командуем боту начать ходить в Telegram за сообщениями
    mybot.start_polling()
    # Запускаем бота, он будет работать, пока мы его не остановим принудительно
    mybot.idle()

# Вызываем функцию main() - именно эта строчка запускает бота
if __name__ == "__main__":
    main()
