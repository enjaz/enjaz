from django.core.urlresolvers import reverse
from django import template
from django.core.exceptions import ObjectDoesNotExist

from bulb import utils

from media.models import RED, GREEN, BLUE, AERO, GREY, ORANGE, YELLOW, PINK, PURPLE

register = template.Library()

@register.filter
def is_bulb_coordinator_or_deputy(user):
    return utils.is_bulb_coordinator_or_deputy(user)

@register.filter
def is_bulb_member(user):
    return utils.is_bulb_member(user)

@register.filter
def can_edit_book(user, book):
    return utils.can_edit_book(user, book)

@register.filter
def can_order_book(user, book):
    return utils.can_order_book(user, book)

@register.filter
def can_edit_group(user, group):
    return utils.can_edit_group(user, group)

@register.filter
def can_join_group(user, group):
    return utils.can_join_group(user, group)

@register.filter
def is_active_group_member(user, group):
    return utils.is_active_group_member(user, group)

@register.filter
def group_can_have_sessions(group):
    return utils.group_can_have_sessions(group)

@register.simple_tag
def reader_profile_link(user):
    try:
        common_profile = user.common_profile
    except ObjectDoesNotExist:
        return user.username

    try:
        reader_profile = user.reader_profile
    except ObjectDoesNotExist:
        return common_profile.get_ar_full_name()

    return u"<a href='{}'>{}</a>".format(reverse('bulb:show_reader_profile',
                                                 args=(user.reader_profile.pk,)),
                                         common_profile.get_ar_full_name())

@register.filter
def can_edit_reader_profile(user, reader_profile):
    return utils.can_edit_reader_profile(user, reader_profile)
