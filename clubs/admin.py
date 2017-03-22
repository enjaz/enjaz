# -*- coding: utf-8  -*-
from django import forms
from django.contrib import admin
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from clubs.models import Club, Team, College
from core.models import StudentClubYear


class ClubFilter(admin.SimpleListFilter):
    title = u"نوع النادي"
    parameter_name = 'type'
    def lookups(self, request, model_admin):
        return (
            ('p', u'الرئاسة'),
            ('s', u'نادي متخصص'),
            ('c', u'نادي كلية'),
            )

    def queryset(self, request, queryset):
        if self.value() == 'p':
            return queryset.filter(english_name__icontains='Presidency')
        elif self.value() == 'c':
            return queryset.exclude(college__isnull=True)
        elif self.value() == 's':
            return queryset.filter(college__isnull=True).exclude(english_name__icontains='Presidency')

class SingleUserChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        try:
            profile = obj.common_profile
            return "%s (%s)" % (obj.username, profile.get_ar_full_name())
        except ObjectDoesNotExist:
            return obj.username

class ClubAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ClubAdminForm, self).__init__(*args, **kwargs)
        if self.instance.id:
            year = self.instance.year
        else:
            year = StudentClubYear.objects.current_year()
        self.fields['parent'].queryset = Club.objects.filter(year=year)
        self.fields['possible_parents'].queryset = Club.objects.filter(year=year)

        media_members = User.objects.filter(memberships__english_name="Media Center",
                                            memberships__year=year) | \
                        User.objects.filter(coordination__english_name="Media Center",
                                            coordination__year=year)
        self.fields['media_assessor'] = SingleUserChoiceField(required=False, queryset=media_members.order_by("username"))

    coordinator = SingleUserChoiceField(required=False, queryset=User.objects.order_by("username"))
    employee = SingleUserChoiceField(required=False, queryset=User.objects.filter(common_profile__is_student=False).order_by("username"))
    media_assessor = SingleUserChoiceField(required=False, queryset=User.objects.order_by("username"))
    class Meta:
        model = Club
        fields = '__all__'

class ClubAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'city', 'email', 'coordinator',
                    'number_of_members', 'get_total_points')
    list_filter = (ClubFilter, 'city', 'gender', 'year')
    search_fields = ('name', 'city', 'email')
    filter_horizontal = ('members', 'deputies',
                         'media_representatives', 'possible_parents')
    form = ClubAdminForm

    def number_of_members(self, obj):
        return obj.members.count()
    number_of_members.short_description = u"عدد الأعضاء"


class CollegeAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'section', 'gender')
    list_filter = ('city', 'gender')

class TeamAdminForm(forms.ModelForm):
    coordinator = SingleUserChoiceField(required=False, queryset=User.objects.order_by("username"))

    class Meta:
        model = Club
        fields = '__all__'

    
class TeamAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'city', 'gender', 'coordinator', 'get_member_count')
    list_filter = ('city', 'gender', 'year')
    search_fields = ('name', 'city', 'gender', 'code_name', 'email')
    filter_horizontal = ('members',)
    form = TeamAdminForm

admin.site.register(College, CollegeAdmin)
admin.site.register(Club, ClubAdmin)
admin.site.register(Team, TeamAdmin)
