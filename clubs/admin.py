from django.contrib import admin
from clubs.models import Club, College
from accounts.admin import deanship_admin

admin.site.register(College)
admin.site.register(Club)
deanship_admin.register(Club)
