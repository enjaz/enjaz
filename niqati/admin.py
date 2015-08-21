# -*- coding: utf-8  -*-
from django.contrib import admin

from niqati.models import Code, Code_Collection, Code_Order

class CodeAdmin(admin.ModelAdmin):
    #list_display = ('code_string', 'collection__parent_order__episode', 'ordering_club', 'collection__code_category', 'user', 'redeem_date',)

    def ordering_club(self, obj):
        return obj.episode.activity.primary_club.name

class CodeCollectionAdmin(admin.TabularInline):
    model = Code_Collection
    extra = 0
    readonly_fields = ('code_category', 'code_count', 'date_downloaded', 'admin_coupon_link', )

class CodeOrderAdmin(admin.ModelAdmin):
    list_display = ('episode', 'ordering_club', 'date_ordered')
    readonly_fields = ('submitter', 'episode', 'ordering_club', 'date_ordered', )
    inlines = (CodeCollectionAdmin, )

    def ordering_club(self, obj):
        return obj.episode.activity.primary_club.name

admin.site.register(Code, CodeAdmin)
admin.site.register(Code_Order, CodeOrderAdmin)
