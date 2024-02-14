import os
import telebot
from telebot import types
from dotenv import load_dotenv
import ast
import json
from datetime import datetime
import time

load_dotenv()

BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

global_step = 0
train_list = ["Off","Treino B","Off","Off"]
global_actions = ["Voltar"]

# trigger on command '/start'
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    btn_01 = types.KeyboardButton(train_list[0])
    btn_02 = types.KeyboardButton(train_list[1])
    btn_03 = types.KeyboardButton(train_list[2])
    btn_04 = types.KeyboardButton(train_list[3])
    markup.add(btn_01, btn_02, btn_03,btn_04)
    
    bot.send_message(message.chat.id, "Qual treino você irá fazer hoje?", reply_markup=markup)
    
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    global global_step, msg, chat_id

    chat_id=message.chat.id
    agora = datetime.now()
    horario_formatado = agora.strftime("%H:%M:%S:%f")
    if(global_step == 0): #start
        if message.text == train_list[0]:
            bot.reply_to(message, "Não implementado")
        elif message.text == train_list[1]:
            global_step = 1
            bot.reply_to(message, "Você escolheu treino B")
            msg = bot.send_message(chat_id,
                     text=f"O treino B - {horario_formatado}",
                     reply_markup=makeKeyboard(),
                     parse_mode='HTML')
        elif message.text == train_list[2]:
            global_step = 1
            bot.reply_to(message, "Não implementado")
        elif message.text == train_list[3]:
            global_step = 1
            bot.reply_to(message, "Não implementado")
        else:
            bot.reply_to(message, "Por favor, escolha uma das opções disponíveis.")

def carregar_dados(caminho_arquivo):
    with open(caminho_arquivo, 'r') as arquivo:
        return json.load(arquivo)

train_a_json = 'treino_a.json'
train_selected = carregar_dados(train_a_json)

confirmIcon = u"\u2705"
editIcon = u"\u2710"
helpIcon = u"\u2754"
awaitIcon = u"\u2573"

def makeKeyboard():
    markup = types.InlineKeyboardMarkup()

    for value in train_selected:
        print('item ', str(value["name"]), str(value['completed']))
        title = types.InlineKeyboardButton(text=value['name'], callback_data="['value', '" + value['name'] + "']")
        edit_button = types.InlineKeyboardButton(text=editIcon, callback_data="['edit', '" + value['name'] + "']") 
        help_button = types.InlineKeyboardButton(text=helpIcon, callback_data="['help', '" + value['url'] + "']") 
        await_button = types.InlineKeyboardButton(text= confirmIcon if value['completed'] else awaitIcon, callback_data="['await', '" + value['name'] + "']") 
        markup.add(title)
        markup.add(edit_button, help_button, await_button) 
    return markup

def completedItem(name):
    for objeto in train_selected:
        if objeto["name"] == name:
            objeto["completed"] = False if objeto["completed"] else True
            return True  
    return False

def getItemByName(name):
    for obj in train_selected:
        if obj["name"] == name:
            return obj
        return False


@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):

    agora = datetime.now()
    current = agora.strftime("%H:%M:%S:%f")

    if (call.data.startswith("['value'")):
        print(f"call.data : {call.data} , type : {type(call.data)}")
        print(f"ast.literal_eval(call.data) : {ast.literal_eval(call.data)} , type : {type(ast.literal_eval(call.data))}")
        valueFromCallBack = ast.literal_eval(call.data)[1]

        currentItem = getItemByName(valueFromCallBack)

        bot.answer_callback_query(callback_query_id=call.id,
                              show_alert=True,
                              text=f"{valueFromCallBack}\nDescrição: {currentItem['description']}\nSeries: {str(currentItem['series'])}\nPeso: {str(currentItem['weight'])}")

    if (call.data.startswith("['edit'")):
        valueFromCallBack = ast.literal_eval(call.data)[1]
        
    if (call.data.startswith("['await'")):
        valueFromCallBack = ast.literal_eval(call.data)[1]
        completedItem(valueFromCallBack)
        bot.edit_message_text(text=f"O treino B - {current}", chat_id=chat_id, message_id=msg.id, reply_markup=makeKeyboard(), parse_mode='HTML')
        
    if (call.data.startswith("['help'")):
        valueFromCallBack = ast.literal_eval(call.data)[1]
        gif_url = ast.literal_eval(call.data)[1]
        helper_img = bot.send_document(call.message.chat.id, gif_url)

        time.sleep(5)
        bot.delete_message(call.message.chat.id, message_id=helper_img.id)


bot.polling()