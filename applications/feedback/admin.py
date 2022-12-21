from django.contrib import admin

from applications.feedback import models

admin.site.register(models.Like)
admin.site.register(models.Rating)
admin.site.register(models.Comment)
admin.site.register(models.Favorite)
