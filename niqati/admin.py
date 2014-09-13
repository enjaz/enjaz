# -*- coding: utf-8  -*-
from django.contrib import admin

from niqati.models import Code, Code_Collection, Code_Order

class CodeAdmin(admin.ModelAdmin):
    list_display = ('code_string', 'activity', 'ordering_club', 'category', 'user', 'redeem_date',)

    def ordering_club(self, obj):
        return obj.activity.primary_club.name

class CodeCollectionAdmin(admin.TabularInline):
    model = Code_Collection
    extra = 0
    readonly_fields = ('code_category', 'code_count', 'delivery_type', 'approved', 'date_created', 'admin_asset_link', )
    exclude = ('asset', )

class CodeOrderAdmin(admin.ModelAdmin):
    list_display = ('activity', 'ordering_club', 'date_ordered')
    readonly_fields = ('activity', 'ordering_club', 'date_ordered', )
    inlines = (CodeCollectionAdmin, )

    def ordering_club(self, obj):
        return obj.activity.primary_club.name

admin.site.register(Code, CodeAdmin)
admin.site.register(Code_Order, CodeOrderAdmin)