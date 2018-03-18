from django.urls import path

from . import views

urlpatterns = [
    path('', views.main, name='main'),
    #path('<category>/', views.category),
    #path('test/<number>', views.test_celery, name='test_celery')
]