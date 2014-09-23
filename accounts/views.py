# -*- coding: utf-8  -*-
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.contrib.auth.models import User

from userena.models import UserenaSignup
from userena.utils import get_datetime_now


class ResendForm(forms.Form):
    email = forms.EmailField()

def resend_confirmation_key(request):
    if request.method == 'POST':
        form = ResendForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email__iexact=email)
                userena_signup = user.userena_signup
            except ObjectDoesNotExist:
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
