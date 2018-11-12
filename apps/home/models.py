from django.core.files.storage import FileSystemStorage
from django.db import models
import os
import time


# 后台管理测试  书籍模型
class Book(models.Model):
    bid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=128, unique=True, db_index=True)

    class Meta:
        db_table = 'book'
        verbose_name = '书籍管理后台'


# --fake 是不执行该迁移脚本但是标记该脚本已经被执行过

# 导航栏模型
class Navigation(models.Model):
    nav_id = models.AutoField(primary_key=True)
    nav_name = models.CharField(max_length=64)

    class Meta:
        db_table = 'navigation'


"""
给图片重名了
"""


# 照片存储模型(用户上传图像文件)
class ImageStorage(FileSystemStorage):
    IMG_PREFIX = 'IMG_'
    FILE_TIME = time.strftime('%Y%m%d%H%M%S')
    from django.conf import settings

    def __init__(self, location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL):
        # 超类初始化
        super().__init__(location, base_url)
        # 重写 _save方法

    # uploaad/img/img_afsfsfds.png
    # 修改文件的名称 重写了父类中保存图片地址的方法
    def _save(self, name, content):
        # 文件扩展名 .jpg  .png 照片文件后缀
        ext_name = name[name.rfind('.'):]
        # 文件目录
        image_path = os.path.dirname(name)
        # 定义文件名，年月日时分秒随机数
        image_name = self.IMG_PREFIX + self.FILE_TIME + ext_name
        image_file = os.path.join(image_path, image_name)
        # 调用父类方法
        return super()._save(image_file, content)


class UserProfile(models.Model):
    phone = models.CharField(max_length=11, default='110')
    desc = models.CharField(max_length=255, null=True)
    uid = models.AutoField('用户ID', primary_key=True)
    icon = models.ImageField(verbose_name=u'头像', max_length=100, upload_to='upload/img/%Y%m%d',
                             default=u"apps/static/img/default.png")
    user = models.OneToOneField('auth.User')

    class Meta:
        db_table = 'user_profile'
        verbose_name = '用户管理'
        verbose_name_plural = verbose_name

    # def img_show(self):
    #     """
    #     后台显示图片
    #     :return:
    #     """
    #     return u'<img width=50px src="%s" />' % self.icon.url
    #
    # img_show.short_description = '头像'
    # # 允许显示HTML tag
    # img_show.allow_tags = True


# 用户评论模型
class Review(models.Model):
    review_id = models.AutoField('ID', primary_key=True)
    content = models.CharField('内容', max_length=4000, )
    create_date = models.DateTimeField('创建时间', auto_now_add=True)
    # 和商品为一对多关系
    shop = models.ForeignKey('Shop', models.DO_NOTHING, db_column='shop_id', db_index=True, verbose_name="商品ID")
    # 和用户也为一对多关系
    user = models.ForeignKey('UserProfile', models.DO_NOTHING, db_column='uid', db_index=True,
                             verbose_name='用户ID')

    class Meta:
        db_table = 'review'
        verbose_name = '用户评论'
        verbose_name_plural = verbose_name


# 轮播图模型
class Banner(models.Model):
    banner_id = models.AutoField('ID', primary_key=True)
    title = models.CharField('标题', max_length=100)
    image = models.ImageField('轮播图', upload_to='banner/%Y%m%d', storage=ImageStorage(), max_length=100)
    detail_url = models.URLField('访问地址', max_length=200)
    order = models.IntegerField('顺序', default=1)
    create_time = models.DateTimeField('添加时间', auto_now_add=True)

    class Meta:
        db_table = 'banner'
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


# 分类菜单模型
class Category(models.Model):
    cate_id = models.AutoField('分类ID',
                               primary_key=True)
    name = models.CharField('名称', max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'category'
        verbose_name = '分类菜单'
        verbose_name_plural = '菜单管理'


# 商品信息模型
class Shop(models.Model):
    shop_id = models.IntegerField(verbose_name='商品ID', primary_key=True)
    name = models.CharField(verbose_name='商品名称', max_length=100)
    sub_title = models.CharField(verbose_name='商品标题', max_length=255)
    original_price = models.DecimalField(verbose_name='原价', max_digits=7, decimal_places=2)
    promote_price = models.DecimalField(verbose_name='折扣价', max_digits=7, decimal_places=2)
    stock = models.IntegerField(verbose_name='库存')
    cate = models.ForeignKey(Category, models.DO_NOTHING, db_column='cate_id', db_index=True, verbose_name='商品分类')
    create_date = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'shop'
        verbose_name = '商品信息'
        verbose_name_plural = '商品管理'


# 订单表模型
class Order(models.Model):
    # 元祖形式
    ORDER_STATUS = (
        (1, '正常'),
        (0, '异常'),
        (-1, '删除'),
    )

    oid = models.AutoField('订单ID', primary_key=True)
    order_code = models.CharField('订单号', max_length=255)
    address = models.CharField('配送地址', max_length=255)
    post = models.CharField('邮编', max_length=255)
    receiver = models.CharField('收货人', max_length=255)
    mobile = models.CharField('手机号', max_length=11)
    user_message = models.CharField('附加信息', max_length=255)
    create_date = models.DateTimeField('创建日期', max_length=0)
    pay_date = models.DateTimeField('支付时间', max_length=0,
                                    blank=True, null=True)
    delivery_date = models.DateTimeField('交易日期', blank=True, null=True)
    confirm_date = models.DateTimeField('确认日期', blank=True, null=True)
    """ 1正常 0 异常, -1 删除 """
    status = models.IntegerField('订单状态', choices=ORDER_STATUS, default=1)
    user = models.ForeignKey('UserProfile', models.DO_NOTHING, db_column='uid', verbose_name="用户ID")

    def __str__(self):
        return self.order_code

    class Meta:
        db_table = 'order'
        verbose_name = '订单'
        verbose_name_plural = '订单管理'


# 商品属性模型
class Property(models.Model):
    property_id = models.AutoField('商品属性', primary_key=True)
    name = models.CharField('属性名称', max_length=64)
    cate = models.ForeignKey(Category, models.DO_NOTHING, db_column='cate_id', db_index=True, verbose_name="父菜单")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'property'
        verbose_name = '商品属性'
        verbose_name_plural = verbose_name


# 商品属性值模型
class PropertyValue(models.Model):
    pro_value_id = models.IntegerField(verbose_name='ID', primary_key=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, db_column='shop_id', verbose_name="商品ID")
    property = models.ForeignKey(Property, on_delete=models.CASCADE, db_column='property_id', verbose_name="属性ID")
    value = models.CharField('属性值', max_length=255)

    def __str__(self):
        return self.value

    class Meta:
        db_table = 'property_value'
        verbose_name = '商品属性值'
        verbose_name_plural = verbose_name


# 购物车表模型
class ShopCar(models.Model):
    car_id = models.AutoField(verbose_name='ID', primary_key=True)
    number = models.IntegerField(verbose_name='商品数量', default=0)
    shop = models.ForeignKey(Shop, models.DO_NOTHING, verbose_name='商品ID')
    user = models.ForeignKey('UserProfile', models.DO_NOTHING, db_column='uid', verbose_name='用户ID')
    order = models.ForeignKey('Order', on_delete=models.SET_NULL, db_column='oid', null=True, verbose_name='商品ID')
    # 1正常 -1 删除 ,0 禁止 2
    status = models.IntegerField(default=1)

    class Meta:
        db_table = 'shop_car'
        verbose_name = '购物车'
        verbose_name_plural = verbose_name


# 商品图片模型
class ShopImage(models.Model):
    shop_img_id = models.AutoField(primary_key=True)
    shop = models.ForeignKey(Shop, models.DO_NOTHING, db_column='shop_id', db_index=True, verbose_name='商品ID')
    type = models.CharField('图片类型', max_length=32, blank=True, null=True)

    def __str__(self):
        return self.shop_img_id

    class Meta:
        db_table = 'shop_image'
        verbose_name = '商品图片'
        verbose_name_plural = '商品图片管理'


# 一级子菜单模型
class SubMenu(models.Model):
    sub_menu_id = models.AutoField('ID', primary_key=True)
    name = models.CharField('名称', max_length=255, blank=True, null=True)
    cate = models.ForeignKey(Category, models.DO_NOTHING, db_column='cate_id', db_index=True,
                             verbose_name='父菜单')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'sub_menu'
        verbose_name = '一级菜单'
        verbose_name_plural = '一级菜单管理'


# 二级子菜单模型
class SubMenu2(models.Model):
    sub_menu2_id = models.AutoField('ID', primary_key=True)
    name = models.CharField('名称', max_length=255)
    sub_menu = models.ForeignKey(SubMenu, models.DO_NOTHING, db_column='sub_menu_id', db_index=True,
                                 verbose_name='父菜单')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'sub_menu2'
        verbose_name = '二级菜单'
        verbose_name_plural = '二级菜单管理'
