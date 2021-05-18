
from django.urls import path

from api import api

app_name = 'celulas'

urlpatterns = [
    path('login/', api.LoginAPI.as_view()),
    path('login-token/', api.LoginPorTokenAPI.as_view()),
]