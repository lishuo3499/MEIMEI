from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile
# Register your models here.
admin.site.register(UserProfile,UserAdmin)#用UserAdmin去注册UserProfile
