# -*- coding: utf-8  -*-
from django.contrib import admin
from .models import *
from core.forms import OptionalForm

# Register your models here.
class PrevousVersionGalleryInline(admin.TabularInline):
    model = Gallery
    form = OptionalForm
    extra = 1


class PrevousVersionAdmin(admin.ModelAdmin):
    inlines = [PrevousVersionGalleryInline]


admin.site.register(PreviousVersion,PrevousVersionAdmin)
admin.site.register(HpcLeader)
admin.site.register(PreviousStatistics)
admin.site.register(Speaker)
admin.site.register(Winner)
admin.site.register(BlogPostArabic)
admin.site.register(BlogPostEnglish)
admin.site.register(BlogVideo)
admin.site.register(FaqQuestion)
admin.site.register(FaqCategory)
admin.site.register(NewsletterMembership)