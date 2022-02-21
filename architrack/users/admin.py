from django.contrib import admin
from .models import Profile, Skill, Year, Course, Location, Modality
# Register your models here.

admin.site.register(Profile)
admin.site.register(Skill)
admin.site.register(Year)
admin.site.register(Course)
admin.site.register(Location)
admin.site.register(Modality)

