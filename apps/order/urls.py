from django.conf.urls import url

from apps.order import views

urlpatterns = [
    url('confirm/', views.confirm_order, name='confirm'),
    url('generate/', views.generate_order, name='generate'),
]
