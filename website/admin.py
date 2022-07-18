from django.contrib import admin
from .models import *


# Register your models here.
admin.site.register(User)
admin.site.register(Episode)
admin.site.register(Podcast)
admin.site.register(List)
admin.site.register(Review)
admin.site.register(Follow)
admin.site.register(ListContent)