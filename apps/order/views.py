import datetime
import random
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect
# django 中获取form表单中多个值  getlist(key)
from Tmall import settings
from apps.home.models import ShopCar, Order


# 确认购买的商品
def confirm_order(request):
    # 获取用户选中商品的记录
    # 获取选择框对象
    # 获取多组number/ck的值 用request.POST.getlist('alias') 返回一个列表迭代器
    checks = request.POST.getlist('ck')

    if checks:
        # 设置字典 check_dict 作用:
        check_dict = {}
        # 设置列表 id_list 作用:
        id_list = []
        # 获取多组数据中的number值
        numbers = request.POST.getlist('number')
        # 获取多组数据中的id
        ids = request.POST.getlist('car_id')
        # 遍历得到的选择框对象 | 如何知道用户选择了哪一个呢？？？
        # 可以通过 forloop.counter0 得到 checks索引 这里得到index索引 就是代表被选择了的商品的序号
        for index in checks:
            # 左边 :被选择的商品的id   |||   右边: 被选择商品的购买数量  利用字典的形式建立起被选择商品的id 和购买数量的关联
            # 这里不能用 key = ids[int(index)]
            # value  = numbers[int(index)]
            # check_list.update(key=value) 因为.update方法中key是支持只读
            # 得到关系绑定添加到字典中
            # 思维方式 为什么？？to do so key : shopcar_id value:shop_number
            check_dict[ids[int(index)]] = numbers[int(index)]
        # 开启数据库事务 遇到错误会回滚
        try:
            with transaction.atomic():
                for key, value in check_dict.items():
                    # 根据用户提交的数据将数据库中ShopCar表中shop_id对应的number更新
                    # 更新不需要对象来接收
                    ShopCar.objects.filter(car_id=int(key)).update(numbers=int(value))
        except:
            pass
    # 如果该条购物车记录被选中  更新数据库中商品的数量
    # 通过用户id(userprofile表中id)和status字段来筛选出
    cars = ShopCar.objects.filter(user_id=request.user.userprofile.uid)
    if cars:
        # 遍历购物车数据多个对象
        for car in cars:
            # 将需要展示的商品信息(img|尺寸|...)与商品绑定
            car.img = car.shop.shopimage_set.all().first()
    return render(request, 'confirm.html', {'cars': cars})


# 查看购物车后 ---> 用户选定需要购买商品 --->返回到确认购买页面  --->将确认购买页面上的信息提交到后台产生订单
def generate_order(request):
    address = request.POST.get('address')
    # 可以选择多种方法支付
    pay_code = request.POST.getlist('rd')
    try:
        with transaction.atomic():
            uid = request.user.userprofile.uid
            # 生成订单号
            order_code = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + str(random.randint(100, 999))
            order = Order(order_code=order_code,
                          address=address,
                          user_message='帮我捎瓶水',
                          mobile='110',
                          user_id=uid,
                          )
            order.save()
            # 用户付款后更新用户购物车数据 改变购物车中status值 更新字段
            # -1 表示已经支付
            ShopCar.objects.filter(user_id=uid, status=1).update(status=-1, order=order)
            if pay_code == 1:
                pass
            else:
                pass
    except:
        pass
    return  HttpResponse('购买成功')


# 结算付款 清空购物车
def pay(request):
    pass

# 点击购买 | 生成订单 | 结算--清空购物车
# @transaction.atomic
# def generate_order(request):
#     # 生成订单号--必须具有唯一性 订单号不能小于八位数
#     # 时间
#     order_code = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + str(random.randint(2000, 90000))


# 以下代码为老师深敲出来的 方法可能不全对
# def pay(request):
#     pay = AliPay(
#         appid=settings.APP_ID,
#         app_private_key_str=settings.PRIVATE_KEY,
#         # 支付宝支付成功后跳转的界面
#         app_notify_url=None,
#         sign_type='RSA2',  # 加密方式
#         debug=False,  # 正式环境改为True，沙箱环境为False
#     )
#     #  生成订单对象
#     order = pay.api_alipay_trade_page_pay(
#         # 订单的描述
#         subject='我，秦始皇，打钱！！',
#         out_trade_no='订单的ID',
#         total_amout='99999999999999.00',
#         return_url='订单支付成功之后的回调地址',
#     )
#     pay_url = settings.ALI_PAY_URL + '?' + order
#     return redirect(pay_url)
#     # 商品的订单 + 商品的总价 + 订单的名称
#
#
# """
#     订单的名称 = 订单 + 订单号 （京东支付方式）
# """
#
#
# # 处理支付成功的函数
# def pay_success(request):
#     pass
