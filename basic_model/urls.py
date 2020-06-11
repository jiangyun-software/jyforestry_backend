from django.urls import path
from . import views

#link urls to the views
urlpatterns = [
    path('', views.test),
]