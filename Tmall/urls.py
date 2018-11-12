from django.conf.urls import url, include
import xadmin

from apps.home import views

urlpatterns = [
    # url('admin/', admin.site.urls),
    #  替换admin为xadmin
    url('xadmin/', xadmin.site.urls),
    # 定位home
    url('home/', include('apps.home.urls')),
    # 定义首页
    url('^$', views.index, name='index'),
    # 搜寻模块
    url('search/', include('apps.search.urls')),
    url('cars/', include('apps.cars.urls')),
    url('account/', include('apps.account.urls')),
    url('order/', include('apps.order.urls')),
]
