from django.contrib import admin
from .models import *

# class SubCourseAdmin(admin.ModelAdmin):
#     list_filter = ['parent_course__name']
#     list_display = ['__unicode__', 'batch_no',
#                     'reg_open_date', 'reg_close_date']
#     search_fields = ['parent_course__name']
#
# admin.site.register(Course)

admin.site.register(HPCVersion)
admin.site.register(Statistic)
admin.site.register(HPCPerson)
admin.site.register(Winner)

