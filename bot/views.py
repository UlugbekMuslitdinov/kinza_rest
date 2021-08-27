from django.http import HttpResponse
import time
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_exempt
import telebot
from telebot import types
from users.models import CustomUser
from .validators import phone_validator, date_validator
from restaurant.models import Category

# =========================================================================================>

TOKEN = '1990088569:AAG1_JT_02jPEI2VZxy5meeOTL2kiOHdRaI'
tbot = telebot.AsyncTeleBot(TOKEN)


# For free PythonAnywhere accounts
# tbot = telebot.TeleBot(TOKEN, threaded=False)

@csrf_exempt
def bot(request):
    if request.META['CONTENT_TYPE'] == 'application/json':

        json_data = request.body.decode('utf-8')
        update = telebot.types.Update.de_json(json_data)
        tbot.process_new_updates([update])

        return HttpResponse("")

    else:
        raise PermissionDenied

# =========================================================================================>


@tbot.message_handler(commands=['start'])
def greet(m):
    get_info = tbot.get_me()
    try:
        user = CustomUser.objects.get(telegram_id=m.chat.id)
    except CustomUser.DoesNotExist:
        tbot.send_message(m.chat.id, 'Hi, we think you are the first time here. Please, send us your name, phone and birthday')
        tbot.register_next_step_handler(m, name_reg)
        get_info.wait()
    else:
        tbot.send_message(m.chat.id, f'Hi, {user.first_name}')
        time.sleep(1)
        markup = types.ReplyKeyboardMarkup(row_width=2)
        markup.add(str(category.name) for category in Category.objects.all())
        tbot.send_message(m.chat.id, "Choose one letter:", reply_markup=markup)
        tbot.register_next_step_handler(m, category_list)


def name_reg(m):
    parts = m.text.split()
    name = parts[0]
    if phone_validator(str(parts[1])):
        phone = parts[1]
        if date_validator(str(parts[2])):
            birthdate = str(parts[2])
            CustomUser.objects.get_or_create(username=phone, defaults={'first_name': name, 'password': birthdate, 'telegram_id': m.chat.id})
            tbot.send_message(m.chat.id, 'Created!')
            markup = types.ReplyKeyboardMarkup(row_width=2)
            markup.add(types.KeyboardButton(i.name) for i in Category.objects.all())
            tbot.send_message(m.chat.id, "Choose one letter:", reply_markup=markup)
            tbot.register_next_step_handler(m, category_list)
        else:
            tbot.send_message(m.chat.id, 'Please check your birthdate and provide all info again')
            tbot.register_next_step_handler(m, name_reg)
    else:
        tbot.reply_to(m, 'Check your phone number and provide all information again')
        tbot.register_next_step_handler(m, name_reg)


def category_list(m):
    pass