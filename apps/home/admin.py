"""
    在admin.py模块中设置|更改与站点管理相关的内容
"""
from xadmin import views
import xadmin

# 主题的修改


# 定义完后需要注册
from apps.home.models import Book


class BaseSystemSettings:
    # 开启修改主题
    enable_themes = True
    use_bootswatch = True


xadmin.site.register(views.BaseAdminView, BaseSystemSettings)


class GlobalSettings:
    site_title = '天猫后台管理系统'
    site_footer = '星球联盟科技有限公司'


xadmin.site.register(views.CommAdminView, GlobalSettings)


# 模型+Admin 默认命名方法
class BookAdmin:
    # 后台管理界面显示的列
    list_display = ['bid', 'name']
    # 搜索的列名
    search_fields = ['name']
    # 分页显示的条数
    list_per_page = 10
    ordering = ['bid']
    # 不允许编辑 readonly:只读字段
    # readonly_fields = ['name']


xadmin.site.register(Book, BookAdmin)
