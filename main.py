import telebot
import re
from telebot import types


bot = telebot.TeleBot('6007128767:AAEefccUAOrmm72ATby_5ybWB2vbIbuJvq4')


@bot.message_handler(commands=['start'])
def start(message):
    keyword = types.InlineKeyboardMarkup()
    item_length = types.InlineKeyboardButton(text='Длина', callback_data='length')
    item_reverse = types.InlineKeyboardButton(text='Перевернуть', callback_data='reverse')
    item_temperature = types.InlineKeyboardButton(text='Температура плавления', callback_data='temperature')
    item_complementary = types.InlineKeyboardButton(text='Комплементарная цепь', callback_data='compl')
    item_gc = types.InlineKeyboardButton(text='GC %', callback_data='gc')
    item_main_info = types.InlineKeyboardButton(text='Длина, Tm, GC%, комплементарная', callback_data='all')

    keyword.add(item_length, item_reverse, item_temperature, item_gc, item_complementary, item_main_info)
    bot.send_message(message.chat.id, 'Что хотите проверить?',
                     reply_markup=keyword)


@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    if call.data == 'length':
        msg = bot.send_message(call.message.chat.id, 'Введите последовательность')
        bot.register_next_step_handler(msg, get_lenght)

    elif call.data == 'temperature':
        msg = bot.send_message(call.message.chat.id, 'Введите последовательность')
        bot.register_next_step_handler(msg, get_tm)

    elif call.data == 'reverse':
        msg = bot.send_message(call.message.chat.id, 'Введите последовательность')
        bot.register_next_step_handler(msg, get_reverse)

    elif call.data == 'compl':
        msg = bot.send_message(call.message.chat.id, 'Введите последовательность')
        bot.register_next_step_handler(msg, get_complementary)

    elif call.data == 'gc':
        msg = bot.send_message(call.message.chat.id, 'Введите последовательность')
        bot.register_next_step_handler(msg, get_gc)

    elif call.data == 'all':
        msg = bot.send_message(call.message.chat.id, 'Введите последовательность')
        bot.register_next_step_handler(msg, get_main_info)


def get_lenght(message):
    msg = bot.send_message(message.chat.id, f"Длина = {len(message.text)}")
    bot.register_next_step_handler(msg, start)


def get_tm(message):

    sequence = str(message.text).lower()
    a = sequence.count('a')
    t = sequence.count('t')
    g = sequence.count('g')
    c = sequence.count('c')

    if len(sequence) > 100:
        bot.send_message(message.chat.id, f"Последовательность слишком длинная. "
                                          f"Максимальная длина = 100 нуклеотидов")
        return None

    elif not re.match("^[ATGCatgc]*$", sequence):
        bot.send_message(message.chat.id, f"Последовательность должна "
                                          f"содержать только символы: A, C, G, T, a, c, g, t")
        return None

    Tm = 2 * (a + t) + 4 * (g + c)
    bot.send_message(message.chat.id, f"Температура плавления = {Tm}")


def get_gc(message):

    sequence = str(message.text).lower()
    g = sequence.count('g')
    c = sequence.count('c')

    if len(sequence) > 500:
        bot.send_message(message.chat.id, f"Последовательность слишком длинная. "
                                          f"Максимальная длина = 500 нуклеотидов")
        return None

    elif not re.match("^[ATGCatgc]*$", sequence):
        bot.send_message(message.chat.id, f"Последовательность должна "
                                          f"содержать только символы: A, C, G, T, a, c, g, t")
        return None

    gc = int(((g + c) / len(sequence)) * 100)
    bot.send_message(message.chat.id, f"GC% = {gc}")


def get_complementary(message):

    sequence = str(message.text).lower()
    complementary = ''

    if len(sequence) > 500:
        bot.send_message(message.chat.id, f"Последовательность слишком длинная. "
                                          f"Максимальная длина = 500 нуклеотидов")
        return None

    elif not re.match("^[ATGCatgc]*$", sequence):
        bot.send_message(message.chat.id, f"Последовательность должна "
                                          f"содержать только символы: A, C, G, T, a, c, g, t")
        return None

    for i in sequence:
        if i == 'a':
            complementary += 'T'
        elif i == 't':
            complementary += 'A'
        elif i == 'g':
            complementary += 'C'
        elif i == 'c':
            complementary += 'G'

    bot.send_message(message.chat.id, f"Комплементарная цепь = {complementary}")


def get_reverse(message):
    sequence = str(message.text).upper()
    bot.send_message(message.chat.id, f"{sequence[::-1]}")


def get_main_info(message):
    get_lenght(message)
    get_tm(message)
    get_gc(message)
    get_complementary(message)


bot.polling(none_stop=True)
