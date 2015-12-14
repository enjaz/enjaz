import functools
from django.shortcuts import render

from accounts.utils import get_user_city


def riyadh_only(view_func):
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not get_user_city(request.user) in ['R', '']:
            return render(request, "studentguide/other-cities.html")
        return view_func(request, *args, **kwargs)
    return wrapper
