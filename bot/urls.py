from django.urls import path

from . import views

urlpatterns = [
    path('', views.handle_request, name='handle_request')
]