from django.contrib import admin
from .models import Gallery, Tag, Region, Category_web,Gender

# Register your models here.
admin.site.register(Gender)
admin.site.register(Gallery)
admin.site.register(Tag)
admin.site.register(Region)
admin.site.register(Category_web)
