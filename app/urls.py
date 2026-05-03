from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path("admin_dashboard",views.admin_dashboard, name="admin_dashboard"),
    # path('thankyou', views.Datasent, name='thank'),
    # path('certification',views.certification,name='certification'),

    path("chatbot/",views.chatbot,name="chatbot"),
    path("login",views.admin_login,name="admin_login"),
]
