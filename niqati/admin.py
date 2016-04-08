# -*- coding: utf-8  -*-
from django.contrib import admin
from niqati.models import Code, Collection, Order

class CodeAdmin(admin.ModelAdmin):
    #list_display = ('code_string', 'collection__parent_order__episode', 'ordering_club', 'collection__code_category', 'user', 'redeem_date',)
    readonly_fields = ('object_id', 'content_type')
    search_fields = ["string", ]

    def ordering_club(self, obj):
        return obj.episode.activity.primary_club.name

class CodeCollectionAdmin(admin.TabularInline):
    model = Collection
    extra = 0
    readonly_fields = ('category', 'code_count', 'date_downloaded', 'admin_coupon_link', )

class CodeOrderAdmin(admin.ModelAdmin):
    list_display = ('episode', 'ordering_club', 'date_ordered')
    readonly_fields = ('submitter', 'episode', 'ordering_club', 'date_ordered', )
    inlines = (CodeCollectionAdmin, )

    def ordering_club(self, obj):
        return obj.episode.activity.primary_club.name

admin.site.register(Code, CodeAdmin)
admin.site.register(Order, CodeOrderAdmin)
