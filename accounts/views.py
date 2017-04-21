# -*- coding: utf-8  -*-
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages

from accounts.forms import EditStudentCommonProfile, ResendForm, EditStudentCommonProfile_NonUser
from clubs.models import city_choices
from userena.models import UserenaSignup


def resend_confirmation_key(request):
    context = {}
    if request.method == 'POST':
        form = ResendForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email__iexact=email)
            except User.DoesNotExist:
                context["error"] = u"nonexistent"
                user = None
            if user:
                if user.is_active:
                    context["error"] = "already_active"
                else:
                    userena_signup = user.userena_signup
                    new_key = UserenaSignup.objects.reissue_activation(userena_signup.activation_key)
                    if new_key:
                        return render(request, 'userena/activate_retry_success.html')
    elif request.method == 'GET':
        pass
    return render(request, 'accounts/resend_confirmation_code.html', context)

@login_required
def edit_common_profile(request):
    try:
        common_profile = request.user.common_profile
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('home'))

    if not request.user.common_profile.profile_type == 'N':
        edit_form = EditStudentCommonProfile
    else:
        edit_form = EditStudentCommonProfile_NonUser


    if request.method == 'POST':
        form = edit_form(request.POST, instance=common_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تعديل بياناتك بنجاح')
            return HttpResponseRedirect(reverse('edit_common_profile'))
    elif request.method == 'GET':
            form = edit_form(request.POST, instance=common_profile)



    if not request.user.common_profile.profile_type == 'N':
        return render(request, 'accounts/edit_common_profile.html', {'form': form,
                                                                 'city_choices': city_choices,
                                                                 'common_profile': common_profile})
    else:
        return render(request, 'accounts/edit_common_profile_nonuser.html', {'form': form,
                                                                 'common_profile': common_profile})
