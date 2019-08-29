from django.contrib import admin

# Register your models here.
from login.models import User,ConfirmString
admin.site.register(User)
admin.site.register(ConfirmString)