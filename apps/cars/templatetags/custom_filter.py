"""
使用自定义过滤器步骤：
    1. 创建templatetags目录
    2. 在创建的templatetags目录中创建py文件
    3. 创建自定义过滤器
        3.1 实例化template.Library()注册对象
        3.2 装饰自定义的过滤器
    4.在模板语法中使用自定义过滤器
        4.1 加载自定义过滤器.py文件
        4.2 {value|过滤器名称:参数}方法使用自定义过滤器
"""
# 导入template模块
from django import template

# 实例化过滤器
register = template.Library()


# value|过滤器名称:参数
@register.filter
def multiply(value, params):
    return value * params
