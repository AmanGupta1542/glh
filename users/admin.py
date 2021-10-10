from django.contrib import admin
from .models import User,Forget_password
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ['id','username','email','password']

class Forget_passwordAdmin(admin.ModelAdmin):
    list_display = ['id','token','current_time','updated_at','user_id']
admin.site.register(User, UserAdmin)
admin.site.register(Forget_password, Forget_passwordAdmin)
