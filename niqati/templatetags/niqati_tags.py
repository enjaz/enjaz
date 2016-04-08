# -*- coding: utf-8  -*-
from django.core.urlresolvers import reverse
from django.template import Library
from django.utils.http import urlquote
import requests

from activities.models import Episode
from bulb.models import Request, Session


register = Library()

@register.simple_tag
def get_short_link(domain, endpoint, code):
    """
    If the code has a short link, then return it.
    Otherwise, generate it and return the result.
    """
    if not code.short_link:
        full_url = urlquote("http://%s%s?code=%s" % (domain, reverse("niqati:submit"), code.string))
        response = requests.get(endpoint + full_url)
        short_link = response.text
        code.short_link = short_link
        code.save()

    return "<a href='%s'>%s</a>" % (code.short_link, code.short_link)

@register.filter
def get_description(code):
    if not code.content_object:
        return u"مُخصّصة ({})".format(code.note)
    elif type(code.content_object) is Episode and code.containing_collections.exists():
        activity_link = u"<a href=\"{}\">{}</a>".format(reverse('activities:show',
                                                               args=(code.content_object.activity.pk,)),
                                                        code.content_object)
        category = code.containing_collections.first().category
        if category.label == "Idea":
            return u"صغت فكرة {}".format(activity_link)
        elif category.label == "Organizer":
            return u"نظّمت {}".format(activity_link)
        elif category.label == "Participation":
            return u"شاركت في {}".format(activity_link)
    elif type(code.content_object) is Request:
        book_link = u"<a href=\"{}\">{}</a>".format(reverse('bulb:show_book',
                                                           args=(code.content_object.book.pk,)),
                                                    code.content_object.book)
        return u"ساهمت بكتاب " + book_link
    elif type(code.content_object) is Session:
        group_link = u"<a href=\"{}\">{}</a>".format(reverse('bulb:show_group',
                                                            args=(code.content_object.group.pk,)),
                                                     code.content_object.group)
        return u"عقدت جلسة {} لمجموعة {}".format(code.content_object.title, group_link)
    else:
        return "<span class=\"english-field\">{}</span>".format(code.string)
