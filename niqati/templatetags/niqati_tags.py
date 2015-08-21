from django.core.urlresolvers import reverse
from django.utils.http import urlquote
import requests
from django.template import Library

register = Library()

@register.simple_tag
def get_short_link(domain, endpoint, code):
    """
    If the code has a short link, then return it.
    Otherwise, generate it and return the result.
    """
    if not code.short_link:
        full_url = urlquote("http://%s%s?code=%s" % (domain, reverse("niqati:submit"), code.code_string))
        response = requests.get(endpoint + full_url)
        short_link = response.text
        code.short_link = short_link
        code.save()

    return "<a href='%s'>%s</a>" % (code.short_link, code.short_link)
