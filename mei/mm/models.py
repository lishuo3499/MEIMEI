from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class UserProfile(AbstractUser):
    jb_num = models.IntegerField(default=10,null=False)
    share_address = models.CharField(max_length=200,null=True)

class User_share(models.Model):
    user_id = models.ForeignKey('UserProfile', related_name='user_share_id', on_delete=models.CASCADE,null=False)
    target_u_ip = models.CharField(max_length=200,null=True)

class Lock_article(models.Model):
    user_id = models.ForeignKey('UserProfile', related_name='user_lock_id', on_delete=models.CASCADE,null=False)
    article_id = models.ForeignKey('Article', related_name='lock_article_id', on_delete=models.CASCADE,null=False)

class Hot_article(models.Model):
    article_id = models.ForeignKey('Article', related_name='hot_article_id', on_delete=models.CASCADE,null=False)


class Img(models.Model):
    img_file = models.ImageField(upload_to='up_load/img')
    file_name = models.CharField(max_length=200,null=True)
    delete_or = models.IntegerField(default=0,null=False)

class Article(models.Model):
    user_id = models.IntegerField(default=0,null=False)
    fm_img =  models.ForeignKey('Img', related_name='fm_img', on_delete=models.CASCADE,null=False)
    title = models.CharField(max_length=200,null=True)
    text = models.CharField(max_length=10000,null=True)
    time = models.DateTimeField(auto_now_add=True)
    tag = models.CharField(max_length=200,null=True)
    classify =  models.ForeignKey('Classify', related_name='classify_art', on_delete=models.CASCADE,null=False)
    classify2 =  models.ForeignKey('Classify', related_name='classify_art2', on_delete=models.CASCADE,null=True)
    delete_or = models.IntegerField(default=0,null=False)
    visit_num = models.IntegerField(default=0,null=False)
    collect_num = models.IntegerField(default=0,null=False)

class Art_img(models.Model):
    article_id =  models.ForeignKey('Article', related_name='article_id', on_delete=models.CASCADE)
    img_id =  models.ForeignKey('Img', related_name='img_id', on_delete=models.CASCADE)


class Collect(models.Model):
    article_id =  models.ForeignKey('Article', related_name='article_collect_id', on_delete=models.CASCADE)
    user_id =  models.ForeignKey('UserProfile', related_name='collect_user_id', on_delete=models.CASCADE)


class Classify(models.Model):
    title = models.CharField(max_length=200,null=False)
    classify = models.CharField(max_length=500,null=False,default='')
    sort = models.IntegerField(default=0,null=True)
    classify_url = models.CharField(max_length=500,null=False,default='')
    classify2 = models.ForeignKey('self', verbose_name='二级菜单', related_name='classify2_c', on_delete=models.CASCADE)
