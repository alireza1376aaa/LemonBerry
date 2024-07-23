from django.contrib import admin
from WebLogSetting.models import Site_Setting,About_us,Contact_Us,photo_page,Team_about
# Register your models here.
admin.site.register(Site_Setting)
admin.site.register(About_us)
admin.site.register(Contact_Us)
admin.site.register(photo_page)
admin.site.register(Team_about)