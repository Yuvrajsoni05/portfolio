from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('thankyou', views.Datasent, name='thank'),
    path('certification',views.certification,name='certification')
]
