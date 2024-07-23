from django.contrib import admin
from .models import web_log, more_discription, Web_log_Comment, Rate_of_Blog


# Register your models here.

class web_log_admin(admin.ModelAdmin):
    x = ['title']
    prepopulated_fields = {
        'slug': x
    }
    list_display = ['id', 'title', 'auter', 'date']
    list_filter = ['gender', 'is_delete', 'date']


admin.site.register(web_log, web_log_admin)
admin.site.register(more_discription)
admin.site.register(Web_log_Comment)
admin.site.register(Rate_of_Blog)
