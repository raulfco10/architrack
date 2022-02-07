from django.contrib import admin

# Register your models here.

from .models import Profile, Skill, Year, Course, Location, Modality

admin.site.register(Profile)
admin.site.register(Skill)
admin.site.register(Year)
admin.site.register(Course)
admin.site.register(Location)
admin.site.register(Modality)
