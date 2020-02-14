from django.contrib import admin

# Register your models here.


from rbac.models import *

class PermissionConfig(admin.ModelAdmin):

    list_display = ["describe", "url", "action", "group"]


admin.site.register(User)
admin.site.register(Permission, PermissionConfig)
admin.site.register(Role)
admin.site.register(PermissionGroup)