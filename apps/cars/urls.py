from django.conf.urls import url

from apps.cars import views

urlpatterns = [
    url('add/', views.add_car, name='add'),
    url('show/', views.show, name='show'),
]
