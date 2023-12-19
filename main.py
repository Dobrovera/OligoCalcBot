import telebot
import re
import os
from telebot import types


TELEGRAM_TOKEN = os.environ.get("SECRET_KEY")
bot = telebot.TeleBot(TELEGRAM_TOKEN)


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
    return None


@bot.message_handler(commands=['help'])
def help_info(message):
    msg = bot.send_message(message.chat.id, 'Привет! \n\nЭтот бот создан для помощи в разработке молекулярно-генетических методик. \n \n'
                                            'Здесь можно проверить длину, температуру плавления, GC% состав праймера, перевернуть последовательность '
                                            'или получить комплементарную цепь.\n\n'
                                            'Рекомендации по дизайну праймеров: \n'
                                            '1. Длина 16-25 нуклеотидов \n'
                                            '2. Содержание пар G-C примерно 40-60% \n'
                                            '3. Температура отжига 40-70С. Лучше, чтобы температура была 50-60С \n'
                                            '4. Разница в температуре отжига в паре праймеров не должна превышать 6°C')
    return None


@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    if call.data == 'length':
        msg = bot.send_message(call.message.chat.id, 'Введите последовательность нуклеотидов')
        bot.register_next_step_handler(msg, get_lenght)

    elif call.data == 'temperature':
        msg = bot.send_message(call.message.chat.id, 'Введите последовательность нуклеотидов '
                                                     '(допустимые символы A, T, G, C, a, t, g, c).\n'
                                                     'Максимальная длина последовательности - 100 нуклеотидов')
        bot.register_next_step_handler(msg, get_tm)

    elif call.data == 'reverse':
        msg = bot.send_message(call.message.chat.id, 'Введите последовательность нуклеотидов')
        bot.register_next_step_handler(msg, get_reverse)

    elif call.data == 'compl':
        msg = bot.send_message(call.message.chat.id, 'Введите последовательность нуклеотидов '
                                                     '(допустимые символы A, T, G, C, a, t, g, c). \n'
                                                     'Максимальная длина последовательности - 500 нуклеотидов')
        bot.register_next_step_handler(msg, get_complementary)

    elif call.data == 'gc':
        msg = bot.send_message(call.message.chat.id, 'Введите последовательность нуклеотидов '
                                                     '(допустимые символы A, T, G, C, a, t, g, c). \n'
                                                     'Максимальная длина последовательности - 500 нуклеотидов')
        bot.register_next_step_handler(msg, get_gc)

    elif call.data == 'all':
        msg = bot.send_message(call.message.chat.id, 'Введите последовательность нуклеотидов '
                                                     '(допустимые символы A, T, G, C, a, t, g, c).')
        bot.register_next_step_handler(msg, get_main_info)
    return None


def get_lenght(message):
    msg = bot.send_message(message.chat.id, f"Длина = {len(message.text)}")
    return None


def get_tm(message):

    sequence = str(message.text).lower()

    if sequence == '/start':
        msg = bot.send_message(message.chat.id, '')
        bot.register_next_step_handler(msg, start)

    elif sequence == '/help':
        bot.register_next_step_handler(message, help_info)

    elif len(sequence) > 100:
        bot.send_message(message.chat.id, f"Расчитать Tm не получилось(\nПоследовательность слишком длинная. "
                                          f"Максимальная длина = 100 нуклеотидов")

    elif not re.match("^[ATGCatgc]*$", sequence):
        bot.send_message(message.chat.id, f"Расчитать Tm не получилось(\nПоследовательность должна "
                                          f"содержать только символы: A, C, G, T, a, c, g, t")

    else:
        a = sequence.count('a')
        t = sequence.count('t')
        g = sequence.count('g')
        c = sequence.count('c')

        Tm = 2 * (a + t) + 4 * (g + c)
        bot.send_message(message.chat.id, f"Температура плавления = {Tm}")

    return None


def get_gc(message):

    sequence = str(message.text).lower()
    g = sequence.count('g')
    c = sequence.count('c')

    if len(sequence) > 500:
        bot.send_message(message.chat.id, f"Расчитать GC состав не получилось(\nПоследовательность слишком длинная. "
                                          f"Максимальная длина = 500 нуклеотидов")

    elif not re.match("^[ATGCatgc]*$", sequence):
        bot.send_message(message.chat.id, f"Расчитать GC состав не получилось(\nПоследовательность должна "
                                          f"содержать только символы: A, C, G, T, a, c, g, t")

    else:
        gc = int(((g + c) / len(sequence)) * 100)
        bot.send_message(message.chat.id, f"GC% = {gc}")
    return None


def get_complementary(message):

    sequence = str(message.text).lower()
    complementary = ''

    if len(sequence) > 500:
        bot.send_message(message.chat.id, f"Получить комплементарную цепь не получилось(\n"
                                          f"Последовательность слишком длинная. "
                                          f"Максимальная длина = 500 нуклеотидов")

    elif not re.match("^[ATGCatgc]*$", sequence):
        bot.send_message(message.chat.id, f"Получить комплементарную цепь не получилось(\n"
                                          f"Последовательность должна "
                                          f"содержать только символы: A, C, G, T, a, c, g, t")

    else:
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
    return None


def get_reverse(message):
    sequence = str(message.text).upper()
    bot.send_message(message.chat.id, f"Перевернутая последовательность - {sequence[::-1]}")
    return None


def get_main_info(message):
    get_lenght(message)
    get_tm(message)
    get_gc(message)
    get_complementary(message)
    return None


bot.polling(none_stop=True)
