from django.urls import path
from . import views

#link urls to the views
urlpatterns = [
    path('', views.test),
    path('form/', views.form),
    path('spreadsheet/', views.SheetUploadView.as_view()),
    path('image/', views.ImageUploadView.as_view()),
]