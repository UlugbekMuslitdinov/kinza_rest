from bot.views import bot
from django.urls import path

urlpatterns = [
    path('cbbf15d8-0421-4512-84d9-5e5d977e3aef/', bot, name="bot"),
]