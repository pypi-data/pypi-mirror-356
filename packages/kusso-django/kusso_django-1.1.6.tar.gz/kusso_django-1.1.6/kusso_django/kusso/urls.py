from django.urls import path
from . import views

app_name = 'kusso'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('authorize/', views.authorize, name='authorize'),
]
