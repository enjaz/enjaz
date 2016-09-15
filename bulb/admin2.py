from django.contrib import admin

from bulb.models import Category, Book, Request, Point, Membership, Group

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

class BookAdmin(admin.ModelAdmin):
    search_fields = ['title', 'submitter__common_profile__en_first_name',
                    'submitter__common_profile__en_middle_name',
                    'submitter__common_profile__en_last_name',
                    'submitter__common_profile__ar_first_name',
                    'submitter__common_profile__ar_middle_name',
                    'submitter__common_profile__ar_last_name']

    list_display = ['pk', 'title', 'submitter', 'category',
                    'is_available',
                    'submission_date']


admin.site.register(Category)
admin.site.register(Book, BookAdmin)
admin.site.register(Request)
admin.site.register(Point)
admin.site.register(Group, GroupAdmin)

