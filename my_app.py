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

def len_mes(text):
    sgn = ',.?/\[]{};:!@#$%^&*()_+=-<>'
    words = text.split(' ')
    new = []
    for word in words:
        if word in sgn:
            continue
        else:
            new.append(word)
    return len(new)

# этот обработчик запускает функцию send_welcome, когда пользователь отправляет команды /start или /help
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.send_message(message.chat.id, "Здравствуйте! Это бот, который посчитает сколько слов в вашем сообщении.")


@bot.message_handler(func=lambda m: True)  # этот обработчик реагирует все прочие сообщения
def send_len(message):
    if message.text == ' ':
        bot.send_message(message.chat.id, 'Ой, попробуй еще раз.')
    else:
        num1 = str(len_mes(message.text))[-1]
        if str(len_mes(message.text)).endswith('1'):
            bot.send_message(message.chat.id, 'В вашем сообщении {} слово.'.format(len_mes(message.text)))
        elif int(num1) < 5:
            bot.send_message(message.chat.id, 'В вашем сообщении {} слова.'.format(len_mes(message.text)))
        else:
            bot.send_message(message.chat.id, 'В вашем сообщении {} слов.'.format(len_mes(message.text)))           
        
    
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
