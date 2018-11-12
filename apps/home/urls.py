from django.conf.urls import url

from apps.home import views

urlpatterns = [
    url('index/', views.index, name='index'),
    # 位置传参
    url('detail/(\d+)/', views.shop_detail, name='detail'),
    # 关键字传参
    # url('detail/(?P<uid>\d+)',views.shop_detail),

]
