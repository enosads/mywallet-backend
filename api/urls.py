from django.urls import path, include
from rest_framework import routers

from api import api

app_name = 'mywallet'

router = routers.DefaultRouter()
router.register('accounts', api.AccountViewSet)
router.register('transactions', api.TransactionViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('login/', api.LoginAPI.as_view()),
    path('login-token/', api.LoginPorTokenAPI.as_view()),
    path('create-usuario/', api.CreateUsuarioAPI.as_view()),
]
