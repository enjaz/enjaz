# -*- coding: utf-8  -*-
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages

from accounts.forms import EditStudentCommonProfile, ResendForm
from clubs.models import city_choices
from userena.models import UserenaSignup
from userena.utils import get_datetime_now


def resend_confirmation_key(request):
    if request.method == 'POST':
        form = ResendForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email__iexact=email)
                userena_signup = user.userena_signup
            except User.DoesNotExist:
                context = {"error": u"nonexistent"}
                return render(request, 'accounts/resend_confirmation_code.html', context)

            if user.is_active:
                context = {"error": "already_active"}
                return render(request, 'accounts/resend_confirmation_code.html', context)

            new_key = UserenaSignup.objects.reissue_activation(userena_signup.activation_key)
            if new_key:
                return render(request, 'userena/activate_retry_success.html')
        else:
            context = {"form": form}
            return render(request, 'accounts/resend_confirmation_code.html', context)

    elif request.method == 'GET':
        return render(request, 'accounts/resend_confirmation_code.html')

@login_required
def edit_common_profile(request):
    try:
        common_profile = request.user.common_profile
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('home'))

    if request.method == 'POST':
        form = EditStudentCommonProfile(request.POST, instance=common_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تعديل بياناتك بنجاح')
            return HttpResponseRedirect(reverse('edit_common_profile'))
    elif request.method == 'GET':
        form = EditStudentCommonProfile(instance=common_profile)

    return render(request, 'accounts/edit_common_profile.html', {'form': form,
                                                                 'city_choices': city_choices,
                                                                 'common_profile': common_profile})

