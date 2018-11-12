from django.shortcuts import render
from apps.home.models import Category, Navigation, Banner, Shop, Review, Property, PropertyValue, ShopCar


# 首页展示相关的函数 必要参数:request
def index(request):
    # 获取分类菜单表中所有数据 返回列表
    categories = Category.objects.all()
    # 获取导航栏菜单中所有数据
    navigations = Navigation.objects.all()
    #  分级绑定 获取分类二级菜单的数据
    for category in categories:

        # 绑定分类菜单与商品表 动态添加属性本来就是动态语言特性之一  一对多关系 选出其子集的前5个[0:5] 绑定在分类对象的shops属性上 二级菜单 category.shops
        category.shops = category.shop_set.all()[0:5]

        # 遍历三级商品列表 将具体商品的图像与其绑定对应上
        for shop in category.shops:
            # 获取商品和其图像并且只选定第一个
            shop.img = shop.shopimage_set.filter(type='type_single').order_by('shop_img_id').first()

        # 将分类菜单的一级菜单与其绑定 找到其一级子菜单
        category.subs = category.submenu_set.all()
        # 遍历其一级菜单
        for sub in category.subs:
            # 将二级菜单与一级菜单绑定
            sub.subs2 = sub.submenu2_set.all()

    # 获取轮播图数据
    banners = Banner.objects.all().order_by('banner_id')

    # 如果用户已经登陆认证 后期用status字段判断
    if request.user.is_authenticated:
        # 如果用户已经登陆 将用户购物车对象计数
        count = ShopCar.objects.filter(user_id=request.user.userprofile.uid).count()
        # 将购物车计数与用户信息一起存储在session|存储在Redis数据库中做缓存
        request.session['count'] = count

    return render(request, 'index.html', {
        'navigations': navigations,
        'banners': banners,
        'categories': categories,

    })


# 思路: 查询具体的商品肯定要知道商品对应的id|标识信息
# 根据商品id获取商品信息
# path   /search/detail/shop_id


# 商品展示详情 根据商品id来展示商品具体信息
def shop_detail(request, id):
    try:
        # 在展示商品的界面中 可以取得商品id信息 # 有必要把query类好好看下
        shop = Shop.objects.get(shop_id=id)
        # 得到商品的图片信息 一对多查询
        shop.imgs = shop.shopimage_set.all()
        # 外键关联 (1)通过对象建立关联 (2)通过数据库中字段 如 shop_id(db_column)进行关联 这里的id就是shop_id
        # 得到商品相关的评论对象
        count = Review.objects.filter(shop_id=id).count()
        # 先查询分类表
        # 再查询产品属性表
        # 再去查询产品的属性值
        # 一对多关系 查询得到的是一个数组 属性分类值 怎么样联系起来的
        properties = Property.objects.filter(cate_id=shop.cate.cate_id)
        for property in properties:
            # 获取具体属性值
            # 查询对应商品的具体属性有哪些和具体属性值
            # 将商品的属性选项和属性值进行绑定
            property.pro_value = PropertyValue.objects.filter(shop_id=id, property_id=property.property_id)

        return render(request, 'shop_detail.html', {'shop': shop, 'count': count, 'properties': properties})
    except Shop.DoesNotExist as e:
        # 此处的错误 Shop.DoesNotExist | Shop.MultipleObjectsReturned 以Shop开头 指的是具体的类 由于get方法自身原因
        print(e)
        pass
    except Shop.MultipleObjectsReturned as e:
        print(e)
