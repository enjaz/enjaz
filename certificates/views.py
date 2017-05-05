# -*- coding: utf-8  -*-
from PIL import Image
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.files.base import ContentFile
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.views.static import serve
from django.shortcuts import render, get_object_or_404

from core import decorators
from certificates.forms import CertificateTemplateForm, CertificateRequestForm, VerifyCertificateForm, PositionFormset
from certificates.models import TEXT_PLACE_HOLDER, CertificateTemplate, CertificateRequest, Certificate, TextPosition
from certificates import utils
from clubs.models import Club
from events.models import Abstract, Session
from niqati.utils import generate_random_string

def index(request):
    return render(request, 'certificates/index.html')

# Certificate views

def list_certificates_per_user(request, pk=None):
    if pk:
        if not utils.can_view_all_certificates(request.user):
            raise PermissionDenied
        else:
            user = get_object_or_404(User, pk=pk)
    else:
        user = request.user

    certificates = Certificate.objects.filter(user=user)
    return render(request, 'certificates/list_certificates.html',
                  {'certificates': certificates})

def show_certificate(request, verification_code):
    certificate = get_object_or_404(Certificate, verification_code=verification_code)
    return render(request, 'certificates/show_certificate.html',
                  {'certificate': certificate})

@login_required
def download_certificate(request, verification_code):
    certificate = get_object_or_404(Certificate,
                                    verification_code=verification_code)

    if not certificate.user and certificate.user == request.user and \
       not utils.can_view_all_certificates(request.user) and \
       not (certificate.content_object and type(certificate.content_object) is Session or \
            certificate.content_object and type(certificate.content_object) is Abstract and\
            is_organizing_team_member(request.user, certificate.content_object.event)):
        raise PermissionDenied       
    
    return serve(request, certificate.image.name, settings.MEDIA_ROOT, show_indexes=False)

def verify_certificate(request):
    context = {}
    if request.method == "POST":
        form = VerifyCertificateForm(request.POST)
        if form.is_valid():
            context['submitted'] = True
            certificate_exists = Certificate.objects.filter(verification_code=verification_code).exists()
            context['certificate_exists'] = certificate_exists
    elif request.method == "GET":
        form = VerifyCertificateForm()
    context['form'] = form 
    return render(request, 'certificates/verify_certificate.html',
                  context)    

# Request views
def list_certificate_requests(request, club_pk=None):
    if club_pk:
        if not utils.can_view_all_certificates(request.user):
            raise PermissionDenied
        else:
            club = get_object_or_404(Club, pk=club_pk)
    else:
        club

    certificate_requests = CertificateRequest.objects.filter(submitter_club=club)
    return render(request, 'certificate_requests/list_certificate_requests.html',
                  {'certificate_requests': certificate_requests})

@login_required
def show_certificate_request(request, pk):
    certificate_request = get_object_or_404(CertificateRequest, pk=pk)
    return render(request, 'certificates/show_certificate_request.html',
                  {'certificate_request': certificate_request})

#@decorators.ajax_only
@login_required
def add_certificate_request(request):
    if request.method == 'POST':
        instance = CertificateRequest(submitter=request.user)
        form = CertificateRequestForm(request.POST, instance=instance, user=request.user)
        if form.is_valid():
            certificate_request = form.save()
            show_url = reverse('certificates:show_certificate_request', args=(certificate_request.pk,))
            return HttpResponseRedirect(show_url)
            #full_url = request.build_absolute_uri(show_url)
            #return {"message": "success", "show_url": full_url}
    elif request.method == 'GET':
        form = CertificateRequestForm(user=request.user)

    context = {'form': form}
    return render(request, 'certificates/add_certificate_request.html', context)
    #return render(request, 'certificates/edit_certificate_request_form.html', context)

#@decorators.ajax_only
@login_required
def edit_certificate_request(request, pk):
    certificate_request = get_object_or_404(CertificateRequest, pk=pk)

    if not utils.can_edit_certificate_request(request.user, certificate_request):
        raise Exception(u"لا تستطيع تعديل المجموعة")

    context = {'certificate_request': certificate_request}
    if request.method == 'POST':
        form = CertificateRequestForm(request.POST, instance=certificate_request, user=request.user)
        if form.is_valid():
            form.save()
            show_url = reverse('certificates:show_certificate_request',
                               args=(certificate_request.pk,))
            return HttpResponseRedirect(show_url)
            #full_url = request.build_absolute_uri(show_url)
            #return {"message": "success", "show_url": full_url}
    elif request.method == 'GET':
        form = CertificateRequestForm(instance=certificate_request, user=request.user)

    context['form'] = form
    return render(request, 'certificates/add_certificate_request.html', context)
    #return render(request, 'certificates/edit_certificate_request_form.html', context)

# Approval views
def approve_request(request, pk):
    if not utils.can_approve_certificates(request.user):
        raise PermissionDenied

    certificate_request = get_object_or_404(CertificateRequest, pk=pk)
    context = {'certificate_request': certificate_request}

    instance = certificate_request.get_template()
    if instance:
        texts = [TEXT_PLACE_HOLDER] * instance.text_positions.count()
        file_path, relative_url = utils.generate_certificate_image(pk,
                                                                   template=instance,
                                                                   texts=texts)
        context['tmp_image'] = relative_url
    else:
        instance = CertificateTemplate(certificate_request=certificate_request)

    if request.method == 'POST':
        template_form = CertificateTemplateForm(request.POST, request.FILES, instance=instance)
        formset = PositionFormset(request.POST, instance=instance)
        if template_form.is_valid() and formset.is_valid():
            template = template_form.save()
            formset.instance = template
            formset.save()
            return HttpResponseRedirect(reverse('certificates:approve_certificate_request', args=(pk,)))
    elif request.method == 'GET':
        template_form = CertificateTemplateForm(instance=instance)
        formset = PositionFormset(instance=instance)

    context['template_form'] = template_form
    context['formset'] = formset

    return render(request, 'certificates/approve_request.html', context)

@csrf_exempt
@decorators.post_only
@decorators.ajax_only
def upload_image(request, pk):
    if not utils.can_approve_certificates(request.user):
        raise PermissionDenied

    template_bytes = request.FILES['image'].read()
    img = Image.open(ContentFile(template_bytes))
    width, height = img.size
    file_path, relative_url = utils.get_temporary_paths(pk)
    with open(file_path, 'w') as f:
        f.write(template_bytes)

    return {'img_url': relative_url, 'width': width, 'height': height}

@csrf_exempt
@decorators.post_only
@decorators.ajax_only
def update_image(request, pk):
    if not utils.can_approve_certificates(request.user):
        raise PermissionDenied

    certificate_request = get_object_or_404(CertificateRequest, pk=pk)

    instance = certificate_request.get_template()
    
    if 'image' in request.FILES:
        template_bytes = request.FILES['image'].read()
    else:
        template_bytes = instance.image.read()

    if instance:
        existing_positions = instance.text_positions.all()
    else:
        existing_positions = TextPosition.objects.none()

    position_formset = PositionFormset(request.POST, instance=instance)
    if position_formset.is_valid():
        # Formsets only return changed objects.
        changed_positions = position_formset.save(commit=False)
        previous_pks = [position.pk for position in changed_positions
                        if position.pk]
        existing_positions = existing_positions.exclude(pk__in=previous_pks)
        positions = changed_positions + list(existing_positions)
    else:
        print position_formset.errors
        raise Exception(u"خطأ في تحديد مواضع النصوص")

    example_text = request.POST.get('example_text', TEXT_PLACE_HOLDER)
    image_format = request.POST.get('image_format', 'PNG')
    template = CertificateTemplate(image_format=image_format)
    texts = [example_text] * len(positions)
    file_path, img_url = utils.generate_certificate_image(certificate_request.pk,
                                                          template=template,
                                                          template_bytes=template_bytes,
                                                          positions=positions,
                                                          texts=texts)
    return {'img_url': img_url}
