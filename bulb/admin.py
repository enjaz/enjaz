from django.contrib import admin

from bulb.models import Category, Book, Request, Point, Membership, Group, Recruitment

class MembershipAdmin(admin.TabularInline):
    model = Membership
    extra = 0
    readonly_fields = ['get_name', ]

    def get_name(self, obj):
        try:
            return obj.user.common_profile.get_ar_full_name()
        except AttributeError:
            return obj.user.username
    get_name.short_description = "Name"

class GroupAdmin(admin.ModelAdmin):
    list_filter = ["is_deleted", ]
    inlines = [MembershipAdmin, ]

admin.site.register(Category)
admin.site.register(Book)
admin.site.register(Request)
admin.site.register(Point)
admin.site.register(Recruitment)
admin.site.register(Group, GroupAdmin)

