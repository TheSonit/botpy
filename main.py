import telebot
import pyowm



owm = pyowm.OWM('1fd33055d6176054ef134e72a7e2baca', language ='ua')
bot = telebot.TeleBot(token)
@bot.message_handler(commands=['weather'])
def question(message):
    chat_id = message.chat.id
    pum = bot.send_message(chat_id, 'Погода в якому місті вас цікавить?')
    bot.register_next_step_handler(pum, weather_sends)

def weather_sends(message):
    observation = owm.weather_at_place(message.text)
    w = observation.get_weather()
    temperature = 'Температура в місті ' + message.text + ' ' + str(w.get_temperature('celsius')['temp']) + ' градусів по Цельсію'
    humidity = 'Вологість ' + str(w.get_humidity()) + '%'
    status = 'Зараз ' + str(w.get_detailed_status())

    degwind = w.get_wind()['deg']
    if (degwind > 22.5) and (degwind < 67.5):
        curse = 'північно-східний'
    elif (degwind >= 67.5) and (degwind <= 112.5):
        curse = 'східний'
    elif (degwind > 112.5) and (degwind < 157.5):
        curse = 'південно-східний'
    elif (degwind >= 157.5) and (degwind <= 202.5):
        curse = 'південний'
    elif (degwind > 202.5) and (degwind < 247.5):
        curse = 'південно-західний'
    elif (degwind >= 247.5) and (degwind <= 292.5):
        curse = 'західний'
    elif (degwind > 292.5) and (degwind < 337.5):
        curse = 'північно-західний'
    else:
        curse = 'північний'

    wind = 'Швидкість вітру ' + str(w.get_wind()['speed']) + ' м/с, напрямок ' + curse
    pressure = 'Тиск ' + str(w.get_pressure()['press']) + ' мбар'

    weather = temperature + '\n \n' + humidity + '\n \n' + status + '\n \n' + wind + '\n \n' + pressure
    bot.send_message(message.chat.id, weather)

bot.polling(none_stop=True)
