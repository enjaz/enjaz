# -*- coding: utf-8  -*-
from __future__ import unicode_literals
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.contrib.auth.models import User

from models import *

# Create your views here.
def view_previous_versions(request):
    versions = HPCVersion.objects.all()
    context = {'versions': versions,}
    return render(request, 'hpc_temp/view_versions.html', context)

def view_version(request, version_id):
    version = HPCVersion.objects.get(pk=version_id)
    context = {'version': version, }
    return render(request, 'hpc_temp/view_version.html', context)