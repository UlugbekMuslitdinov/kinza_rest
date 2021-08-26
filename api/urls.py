from django.urls import path
from .views import DishAPIView, CategoryAPIView, CategoryDetailView

app_name = 'api'
urlpatterns = [
    path('dish/', DishAPIView.as_view()),
    path('category/<str:pk>', CategoryDetailView.as_view()),
    path('', CategoryAPIView.as_view()),
]