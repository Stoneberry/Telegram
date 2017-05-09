# -*- coding: utf-8 -*-
import flask
import telebot
import conf

WEBHOOK_URL_BASE = "https://{}:{}".format(conf.WEBHOOK_HOST, conf.WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}/".format(conf.TOKEN)

bot = telebot.TeleBot(conf.TOKEN, threaded=False)  # бесплатный аккаунт pythonanywhere запрещает работу с несколькими тредами

# удаляем предыдущие вебхуки, если они были
bot.remove_webhook()

# ставим новый вебхук = Слышь, если кто мне напишет, стукни сюда — url
bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH)

app = flask.Flask(__name__)

# этот обработчик запускает функцию send_welcome, когда пользователь отправляет команды /start или /help
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.send_message(message.chat.id, "Здравствуйте! Это бот, который считает сколько слов в вашем сообщении!")

def len_text(text):
        text1 = text.split(' ')
        alf = ':;"?><,.*()&^%$#@!{}{]\|/'
        x1 = []
        for i in text1:
                if i in alf:
                        continue
                else:
                        x1.append(i)
        return len(x1)
   
@bot.message_handler(func=lambda m: True)  # этот обработчик реагирует на любое сообщение
def send_len(message):
        if str(len_text(message.text)).endswith(1):
                bot.send_message(message.chat.id, 'В вашем сообщении {} слово.'.format(len_text(message.text)))
        elif len_text(message.text) < 5:
                bot.send_message(message.chat.id, 'В вашем сообщении {} слова.'.format(len_text(message.text)))
        else:
                bot.send_message(message.chat.id, 'В вашем сообщении {} слов.'.format(len_text(message.text)))


# пустая главная страничка для проверки
@app.route('/', methods=['GET', 'HEAD'])
def index():
    return 'ok'

# обрабатываем вызовы вебхука = функция, которая запускается, когда к нам постучался телеграм 
@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)
##        
##if __name__ == '__main__':
##    bot.polling(none_stop=True)
