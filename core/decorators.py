import functools
import logging
import json

from django.http import HttpResponse, HttpResponseForbidden, Http404
from django.core import exceptions as django_exceptions

# Slightly modified copy of:
# https://github.com/ASKBOT/askbot-devel/blob/85a833860e8915474abbbcb888ab99a1c2300e2c/askbot/utils/decorators.py
# Check student-portal README file for copyrigth details.
def get_only(view_func):
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.method != 'GET':
            raise django_exceptions.PermissionDenied(
                'request method %s is not supported for this function' % \
                request.method
            )
        return view_func(request, *args, **kwargs)
    return wrapper

def post_only(view_func):
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.method != 'POST':
            raise django_exceptions.PermissionDenied(
                'request method %s is not supported for this function' % \
                request.method
            )
        return view_func(request, *args, **kwargs)
    return wrapper

def ajax_only(view_func):
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.is_ajax():
            raise Http404
        try:
            data = view_func(request, *args, **kwargs)
            if data is None:
                data = {}
        except Exception, e:
            #todo: also check field called "message"
            if hasattr(e, 'messages'):
                if len(e.messages) > 1:
                    message = u'<ul>' + \
                        u''.join(
                            map(lambda v: u'<li>%s</li>' % v, e.messages)
                        ) + \
                        u'</ul>'
                else:
                    message = e.messages[0]
            else:
                message = unicode(e)
            if message == '':
                message = 'Oops, apologies - there was some error'
            logging.debug(message)
            data = {
                'message': message,
                'success': 0
            }
            return HttpResponse(json.dumps(data), content_type='application/json')

        if isinstance(data, HttpResponse):#is this used?
            data.mimetype = 'application/json'
            return data
        else:
            data['success'] = 1
            json_data = json.dumps(data)
            return HttpResponse(json_data, content_type='application/json')
    return wrapper
