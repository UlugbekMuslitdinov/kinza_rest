from django.http import HttpResponse
import time
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_exempt
import telebot
from telebot import types
from users.models import CustomUser
from .validators import phone_validator, date_validator
from restaurant.models import Category, Dish

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
        tml_list = [f'{category.name}' for category in Category.objects.all()]
        markup.add(*tml_list)
        tbot.send_message(m.chat.id, "Choose one letter:", reply_markup=markup)
        tbot.register_next_step_handler(m, category_detail)


def name_reg(m):
    parts = m.text.split()
    name = parts[0]
    if phone_validator(str(parts[1])):
        phone = parts[1]
        if date_validator(str(parts[2])):
            birthdate = str(parts[2])
            CustomUser.objects.get_or_create(username=phone, defaults={'first_name': name, 'password': birthdate, 'telegram_id': m.chat.id})
            tbot.send_message(m.chat.id, 'Created!')
            time.sleep(1)
            markup = types.ReplyKeyboardMarkup(row_width=2)
            tml_list = [f'{category.name}' for category in Category.objects.all()]
            markup.add(*tml_list)
            tbot.send_message(m.chat.id, "Choose one letter:", reply_markup=markup)
            tbot.register_next_step_handler(m, category_detail)
        else:
            tbot.send_message(m.chat.id, 'Please check your birthdate and provide all info again')
            tbot.register_next_step_handler(m, name_reg)
    else:
        tbot.reply_to(m, 'Check your phone number and provide all information again')
        tbot.register_next_step_handler(m, name_reg)


def category_detail(m):
    category_name = m.text
    try:
        category = Category.objects.get(name=str(category_name))
    except Category.DoesNotExist:
        tbot.reply_to(m, 'This category does not exist. Please choose once more')
        tbot.register_next_step_handler(m, category_detail)
    else:
        category_dishes = Dish.objects.filter(category=category)
        tmp_list = [f'{dish.name}' for dish in category_dishes]
        markup = types.ReplyKeyboardMarkup(row_width=5)
        markup.add(*tmp_list)
        tbot.send_message(m.chat.id, 'Choose dish:', reply_markup=markup)
        tbot.register_next_step_handler(m, dish_detail)


def dish_detail(m):
    dish_name = m.text
    try:
        dish = Dish.objects.get(name=str(dish_name))
    except Dish.DoesNotExist:
        tbot.reply_to(m, 'This dish name is incorrect. Choose it once more')
        tbot.register_next_step_handler(m, dish_detail)
    else:
        photo = open(str(dish.image.url), 'rb')
        tbot.send_photo(m.chat.id, photo)
        time.sleep(1)
        tbot.send_message(m.chat.id, f'{dish.price}')