from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime

# Create your models here.


class CommonModel(models.Model):
    create_time = models.DateTimeField(verbose_name='创建时间', null=True, blank=True)
    update_time = models.DateTimeField(verbose_name='更新时间', null=True, blank=True)

    class Meta:
        abstract = True


class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50, default="", verbose_name='昵称', db_column='nickname')
    image = models.ImageField(upload_to='image/%Y/%m', default='', max_length=120)
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name='手机号码')
    address = models.CharField(max_length=200, null=True, blank=True, verbose_name='个人地址')
    sex = models.CharField(choices=[('man', '男人'), ('woman', '女人')], default='man', max_length=50)

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.username


class Category(CommonModel):
    title = models.CharField(verbose_name='标题', null=True, blank=True, max_length=50)
    path = models.CharField(verbose_name='路径', null=True, blank=True, max_length=120)
    pid = models.IntegerField(verbose_name='父id', null=True, blank=True)

    class Meta:
        db_table = 'category'
        verbose_name = '分类名称'
        verbose_name_plural = verbose_name


class Product(CommonModel):

    status_active = 'active'
    status_inactive = 'inactive'

    cate = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(verbose_name='产品标题', null=True, blank=True, max_length=50)
    price = models.DecimalField(verbose_name='产品单价', null=True, blank=True, max_digits=8, decimal_places=2)
    status = models.CharField(choices=[(status_active, '启用'), (status_inactive, '禁用')], default=status_active, max_length=50)
    storage_num = models.IntegerField(verbose_name='产品库存数量', null=True, blank=True)
    Sales_num = models.IntegerField(verbose_name='产品销售数量', null=True, blank=True)
    specification = models.CharField(verbose_name='产品规格', null=True, blank=True, max_length=1000)

    class Meta:
        db_table = 'product'
        verbose_name = '产品表'
        index_together = ['title', 'price']


class Image(CommonModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    img_path = models.CharField(verbose_name='图片地址', null=True, blank=True, max_length=200)
    title = models.CharField(verbose_name='图片名称', null=True, blank=True, max_length=50)

    class Meta:
        db_table = 'image'
        verbose_name = '产品图片'


class Banner(models.Model):
    title = models.CharField(max_length=100, verbose_name=u"标题")
    image = models.ImageField(upload_to="banner/%Y/%m", verbose_name=u"轮播图", max_length=100)
    url = models.URLField(max_length=200, verbose_name=u"访问地址")
    index = models.IntegerField(default=100, verbose_name=u"顺序")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        db_table = 'banner'
        verbose_name = u"轮播图"
        verbose_name_plural = verbose_name
