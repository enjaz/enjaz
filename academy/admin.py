from django.contrib import admin
from .models import *

class SubCourseAdmin(admin.ModelAdmin):
    list_filter = ['parent_course__name']
    list_display = ['__unicode__', 'batch_no',
                    'reg_open_date', 'reg_close_date']
    search_fields = ['parent_course__name']

class InstructorAdmin(admin.ModelAdmin):
    raw_id_fields = ['user']

class GraduateAdmin(admin.ModelAdmin):
    raw_id_fields = ['user']

class NewStudentAdmin(admin.ModelAdmin):
    raw_id_fields = ['user']

admin.site.register(Course)
admin.site.register(SubCourse, SubCourseAdmin)
admin.site.register(Instructor, InstructorAdmin)
admin.site.register(Graduate, GraduateAdmin)
admin.site.register(Media_File)
admin.site.register(Work)
admin.site.register(NewStudent, NewStudentAdmin)
admin.site.register(IndexBG)
admin.site.register(Temporary_Stats)