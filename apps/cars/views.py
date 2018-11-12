from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from apps.home.models import ShopCar


@login_required
def add_car(request):
    try:
        # request.user是request对象封装的与auth_user相关的方法
        # auth_user是主表 userprofile是从表
        # 一对一关系查询 查询主表 FO.FK
        # 主表对象查询从表对象  MO.CL
        # 向购物车中添加商品 需要信息: 用户| 商品| 商品数量
        uid = request.user.userprofile.uid
        # 注意获取到的数据类型
        num = int(request.GET.get('num'))
        shop_id = int(request.GET.get('shop_id'))
        # 两步操作
        # 如果商品不在购物车里  创建购物车对象
        # 如果对象存在购物车中 商品数量+
        """
            需求:
              用户在添加商品时 只是刷新与购物车相关的变量 而不是全局刷新(要求局部刷新)
        """
        # 获取用户添加商品的购物车对象
        cars = ShopCar.objects.filter(user=request.user.userprofile, shop_id=shop_id)

        if cars:
            # 一对多 得到QuerySet对象
            # 得到对应商品的购物车对象
            car = cars.first()
            # 当此商品购物车对象存在 那么当此购买商品的数量进行累加
            car.number += num
            car.save()
        else:

            # 绑定用户| 商品 | 商品数量 创建购物车对象
            car = ShopCar(user_id=request.user.userprofile.uid, shop_id=shop_id, number=num)
            car.save()
            # 将用户相关信息存储在session中 用redis来做session
            request.session['count'] += 1
        # 返回数据后停留在原界面 所以不是重新返回模板
        return HttpResponse('success')
    except Exception as e:
        print(e)
        return HttpResponse('failed')


# 需要展示在购物车界面得信息: 商品的图片| 商品的名称 | 商品的价格 | 商品的数量
@login_required
def show(request):
    # 根据自身用户id查询用户的购物车信息
    cars = ShopCar.objects.filter(user_id=request.user.userprofile.uid)
    # 获取商品的图片信息
    for car in cars:
        # car 购物车和shop表是多对一 shop表和shopimage是一对多 这里只取第一张照片展示
        # 将购物车里的每条购物数据都动态绑定.img属性 调用查看
        car.img = car.shop.shopimage_set.all().first()
    return render(request, 'cars.html', {'cars': cars})
