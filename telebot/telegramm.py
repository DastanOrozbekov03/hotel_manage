import telebot
from telebot import types, callback_data

bot = telebot.TeleBot('7179675407:AAEmeRNVIqUkJAMKujaq7mglXQk0zmOZS9Q')

@bot.message_handler(commands=['start'])
def button(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    item = types.InlineKeyboardButton('ДА', callback_data='answer_1')
    item2 = types.InlineKeyboardButton('НЕТ', callback_data='answer_2')
    markup.add(item, item2)
    bot.send_message(message.chat.id, 'Здравствуйте, хотите узнать информацию об отелях ?', reply_markup=markup)

@bot.callback_query_handler(func= lambda call: True)
def answer(call):
    if call.data == 'answer_1':
        markup_reply = types.ReplyKeyboardMarkup(resize_keyboard= True)
        item3 = types.KeyboardButton(text='NOVOTEL')
        item4 = types.KeyboardButton(text='SHERATON')
        item5 = types.KeyboardButton(text='GOLDEN DRAGON')
        item6 = types.KeyboardButton(text='DAMAS')
        item7 = types.KeyboardButton(text='SMART')

        markup_reply.add(item3, item4, item5, item6, item7)
        bot.send_message(call.message.chat.id, 'Нажмите на одну из кнопок', reply_markup=markup_reply)
    elif call.data == 'answer_2':
        bot.send_message(call.message.chat.id, 'ПОКА :)')


@bot.message_handler(content_types=['text'])
def get_text(message):
    if message.text == 'NOVOTEL':
        markup_reply2 = types.ReplyKeyboardMarkup(resize_keyboard= True)
        item8 = types.KeyboardButton(text='ЦЕНА NOVOTEL')
        item9 = types.KeyboardButton(text='АДРЕС NOVOTEL')
        markup_reply2.add(item8, item9)
        bot.send_message(message.chat.id, 'Выберите:', reply_markup=markup_reply2)
    if message.text == 'ЦЕНА NOVOTEL':
        bot.send_message(message.chat.id, f"1000$ за один день в нашем отеле")
    elif message.text == 'АДРЕС NOVOTEL':
        bot.send_message(message.chat.id, f"Адрес: 16 просп. Манаса, Бишкек 720010")
    elif message.text == 'SHERATON':
        markup_reply3 = types.ReplyKeyboardMarkup(resize_keyboard= True)
        item10 = types.KeyboardButton(text='ЦЕНА SHERATON')
        item11 = types.KeyboardButton(text='АДРЕС SHERATON')
        markup_reply3.add(item10, item11)
        bot.send_message(message.chat.id, 'Выберите:', reply_markup=markup_reply3)
    if message.text == 'ЦЕНА SHERATON':
        bot.send_message(message.chat.id, f"1000$ за один день в нашем отеле") 
    elif message.text == 'АДРЕС SHERATON':
        bot.send_message(message.chat.id, f"Адрес: 148B Kievskaya Str, 720001")
    elif message.text == 'GOLDEN DRAGON':
        markup_reply4 = types.ReplyKeyboardMarkup(resize_keyboard= True)
        item12 = types.KeyboardButton(text='ЦЕНА GD')
        item13 = types.KeyboardButton(text='АДРЕС GD')
        markup_reply4.add(item12, item13)
        bot.send_message(message.chat.id, 'Выберите:', reply_markup=markup_reply4)
    if message.text == 'ЦЕНА GD':
        bot.send_message(message.chat.id, f"1000$ за один день в нашем отеле") 
    elif message.text == 'АДРЕС GD':
        bot.send_message(message.chat.id, f"Адрес: 60 ул. Мукая Элебаева, Бишкек 720005")
    elif message.text == 'DAMAS':
        markup_reply5 = types.ReplyKeyboardMarkup(resize_keyboard= True)
        item14 = types.KeyboardButton(text='ЦЕНА DAMAS')
        item15 = types.KeyboardButton(text='АДРЕС DAMAS')
        markup_reply5.add(item14, item15)
        bot.send_message(message.chat.id, 'Выберите:', reply_markup=markup_reply5)
    if message.text == 'ЦЕНА DAMAS':
        bot.send_message(message.chat.id, f"1000$ за один день в нашем отеле") 
    elif message.text == 'АДРЕС DAMAS':
        bot.send_message(message.chat.id, f"Адрес: 107 Жумабек, Бишкек 720001")
    elif message.text == 'SMART':
        markup_reply6 = types.ReplyKeyboardMarkup(resize_keyboard= True)
        item16 = types.KeyboardButton(text='ЦЕНА SMART')
        item17 = types.KeyboardButton(text='АДРЕС SMART')
        markup_reply6.add(item16, item17)
        bot.send_message(message.chat.id, 'Выберите:', reply_markup=markup_reply6)
    if message.text == 'ЦЕНА SMART':
        bot.send_message(message.chat.id, f"1000$ за один день в нашем отеле") 
    elif message.text == 'АДРЕС SMART':
        bot.send_message(message.chat.id, f"Адрес: 204 ул. Юсупа Абдрахманова, Бишкек 720040")

bot.polling()