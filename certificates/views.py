# -*- coding: utf-8  -*-
from PIL import Image
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.core.files.base import ContentFile
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
import cStringIO
import base64

from core import decorators
from certificates.forms import CertificateTemplateForm, CertificateRequestForm, VerifyCertificateForm
from certificates.models import CertificateTemplate, CertificateRequest, Certificate
from certificates import utils
from clubs.models import Club
from niqati.utils import generate_random_string

def index(request):
    return render(request, 'certificates/index.html')
    

# Certificate views

def list_certificates(request, username=None):
    if username:
        if not utils.can_view_all_certificates(request.user):
            raise PermissionDenied
        else:
            user = get_object_or_404(User, username=username)
    else:
        user = request.user

    certificates = Certificate.objects.filter(user=user)
    return render(request, 'certificates/list_certificates.html',
                  {'certificates': certificate})

def show_certificate(request, verification_code):
    certificate = get_object_or_404(Certificate, verification_code=verification_code)
    return render(request, 'certificates/show_certificate.html',
                  {'certificate': certificate})

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
    try:
        instance = certificate_request.certificatetemplate
    except ObjectDoesNotExist:
        instance = CertificateTemplate(certificate_request=certificate_request,
                                       description=certificate_request.description)

    context = {'certificate_request': certificate_request,
               'certificate_template': instance}

    if request.method == 'POST':
        form = CertificateTemplateForm(request.POST, instance=instance)
        if form.is_valid() and 'template_image' in request.session:
            certificate_template = form.save()
            if form.cleaned_data['is_approved']:
                certificate_request.is_approved = True
                template_bytes = base64.b64decode(request.session['template_image'])
                filename = u"{}.{}".format(certificate_template.description, certificate_template.image_format)
                template_file = ContentFile(template_bytes)
                certificate_template.image.save(filename, template_file)
                for student in certificate_request.students.all():
                    print student
                    template_file = ContentFile(template_bytes)

                    while True:
                        verification_code = generate_random_string(6)
                        if not Certificate.objects.filter(verification_code=verification_code).exists():
                            break

                    img_response = utils.generate_certificate_image(template_bytes,
                                                              certificate_template.image_format,
                                                              certificate_template.y_position,
                                                              certificate_template.x_position,
                                                              student.common_profile.get_en_full_name(),
                                                              certificate_template.color,
                                                              certificate_template.font_size)
                    certificate = Certificate.objects.create(certificate_template=certificate_template,
                                                             user=student,
                                                             verification_code=verification_code)
                    certificate_file = ContentFile(img_response)
                    certificate.image.save("{}.{}".format(certificate.pk, certificate_template.image_format), certificate_file)

        elif not 'template_image' in request.session:
            context['error'] = 'no_image'
        else:
            print form.errors
    elif request.method == 'GET':
        form = CertificateTemplateForm(instance=instance)

    context['form'] = form
    print form.errors
    return render(request, 'certificates/approve_request.html', context)

def delete_template(request, pk):
    certificate_request = get_object_or_404(CertificateRequest, pk=pk)

    if not utils.can_approve_certificates(request.user):
        raise PermissionDenied

    if 'template_image' in request.session:
        del request.session['template_image']

    CertificateTemplate.objects.filter(certificate_request=certificate_request).delete()
    show_url = reverse('certificates:show_certificate_request', args=(certificate_request.pk,))
    return HttpResponseRedirect(show_url)

@csrf_exempt
@decorators.post_only
@decorators.ajax_only
def upload_image(request, pk):
    if not utils.can_approve_certificates(request.user):
        raise PermissionDenied
    #certificate_request = get_object_or_404(CertificateRequest, pk=pk)
    template_bytes = request.FILES['image'].read()
    img = Image.open(ContentFile(template_bytes))
    width, height = img.size
    img_str = base64.b64encode(template_bytes)
    request.session['template_image'] = img_str
    request.session['width'] = width
    request.session['height'] = height

    return {'img_str': img_str, 'width': width, 'height': height}

@csrf_exempt
@decorators.post_only
@decorators.ajax_only
def save_image(request, pk):
    if not utils.can_approve_certificates(request.user):
        raise PermissionDenied

    certificate_request = get_object_or_404(CertificateRequest, pk=pk)
    template_bytes = base64.b64decode(request.session['template_image'])
    img_file = ContentFile(template_bytes)
    instance = CertificateTemplate(certificate_request=certificate_request)
    form = CertificateTemplateForm(request.POST, instance=CertificateTemplate)
    if form.is_valid():
        certificate_template = form.save()
        print "it works!"
        certificate_template.image.save(request.POST['title']+certificate_template.image_format, img_file)
    else:
        print form.errors
    return {}

@csrf_exempt
@decorators.post_only
@decorators.ajax_only
def update_image(request, pk):
    if not utils.can_approve_certificates(request.user):
        raise PermissionDenied
    certificate_request = get_object_or_404(CertificateRequest, pk=pk)

    if 'template_image' in  request.session:
        template_bytes = base64.b64decode(request.session['template_image'])
    else:
        # FIXME: Handle when no certificate template was saved.
        template_bytes = certificate_request.certificatetemplate.image.read()

    y_position = float(request.POST['y'])
    x_position = float(request.POST['x'])
    example_text = request.POST.get('example_text', 'Nada Abdullah')
    image_format = request.POST.get('image_format', 'PNG')
    color = request.POST['color']
    try:
        font_size = int(request.POST['font_size'])
    except ValueError:
        raise Exception(u"لم تدخل حجما صالحا للخط")
    img_response = utils.generate_certificate_image(template_bytes,
                                              image_format,
                                              y_position,
                                              x_position,
                                              example_text,
                                              color,
                                              font_size)
    img_str = base64.b64encode(img_response.getvalue())
    return {'img_str': img_str}
