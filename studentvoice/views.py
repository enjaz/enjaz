# -*- coding: utf-8  -*-
import datetime

from django import forms
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import permission_required, login_required
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.views.decorators import csrf


from core import decorators
from studentvoice.models import Voice, Vote, View

# As a general design decision, the user interface (which can also be
# used by admins), will disply both published and pending-revision
# voices.  Deleted voices will be shown only in the admin interface.
# This makes things slighly cleaner since the deleted voices were
# intentionally deleted and thus no need to show them every time.

class VoiceForm(forms.ModelForm):
    # Redefine the fields for them to be required.
    title = forms.CharField(max_length=Voice._meta.get_field('title').max_length,
                            label=Voice._meta.get_field('title').verbose_name)
    recipient = forms.CharField(max_length=Voice._meta.get_field('recipient').max_length,
                            label=Voice._meta.get_field('recipient').verbose_name)
    class Meta:
        model = Voice
        fields = ['title', 'text', 'recipient']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Voice
        fields = ['text']

@login_required
def home(request):
    if request.user.is_authenticated():
        template = 'studentvoice_base.html'
    else:
        template = 'front/front_base.html'

    # parent__isnull=True: Only show original voices, not comments.
    # Also, if the user has the view_voice permission, show voices
    # that are pending-revision.
    if request.user.has_perm('studentvoice.view_voice'):
        voices = Voice.objects.filter(parent__isnull=True,
                                      is_published__in=[True, None])
    else:
        voices = Voice.objects.filter(parent__isnull=True,
                                      is_published=True)

    voice_filter = request.GET.get('filter')
    if voice_filter == 'mine':
        filtered_voices = voices.filter(submitter=request.user)
    elif voice_filter == 'day':
        one_day_ago = datetime.datetime.now() - datetime.timedelta(days=1)
        filtered_voices = voices.filter(submission_date__gte=one_day_ago)
    elif voice_filter == 'week':
        one_week_ago = datetime.datetime.now() - datetime.timedelta(days=7)
        filtered_voices = voices.filter(submission_date__gte=one_week_ago)
    elif voice_filter == 'motnh':
        one_month_ago = datetime.datetime.now() - datetime.timedelta(days=30)
        filtered_voices = voices.filter(submission_date__gte=one_month_ago)
    else:
        filtered_voices = voices

    voice_order = request.GET.get('order')
    if voice_order == 'score':
        ordered_voices = filtered_voices.order_by('-score')
    elif voice_order == 'comments':
        ordered_voices = filtered_voices.order_by('-number_of_comments')
    elif voice_order == 'views':
        ordered_voices = filtered_voices.order_by('-number_of_views')
    else:
        ordered_voices = filtered_voices.order_by('-submission_date')

    # Each page of results should have a maximum of 25 activities.
    paginator = Paginator(ordered_voices, 25)
    page = request.GET.get('page')

    try:
        page_voices = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page_voices = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page_voices = paginator.page(paginator.num_pages)

    context = {'page_voices': page_voices, 'template': template}
    return render(request, 'studentvoice/list.html', context)

@login_required
@permission_required('studentvoice.add_vote', raise_exception=True)
@csrf.csrf_exempt
@decorators.ajax_only
@decorators.post_only
def vote(request):
    voice_id = request.POST.get('voice_id')
    vote_type = request.POST.get('vote_type')
    if not voice_id or not type:
        raise Exception(u'حدث خطأ!')

    if vote_type == 'U':
        opposte_vote_type = 'D'
    elif vote_type == 'D':
        opposte_vote_type = 'U'

    voice = get_object_or_404(Voice, pk=voice_id)
    greatest_parent = voice.get_greatest_parent()

    if not voice.is_published or not greatest_parent.is_published:
        raise Exception(u'لا يمكنك التصويت على صوت غير منشور.')

    if voice.submitter == request.user:
        raise Exception(u'لا يمكنك التصويت على آرائك.')

    try:
        previous_vote = Vote.objects.get(submitter=request.user,
                                         voice=voice)
    except ObjectDoesNotExist:
        previous_vote = None

    if previous_vote:
        # If the previous vote was of the same type, don't accept it.
        if previous_vote.vote_type == vote_type:
            raise Exception(u'صوت سابقا')
        elif previous_vote.vote_type == opposte_vote_type:
            previous_vote.vote_type = vote_type
            previous_vote.save()
    else:
        Vote.objects.create(submitter=request.user, voice=voice,
                            vote_type=vote_type)
    return {'score': voice.update_score()}

@login_required
@permission_required('studentvoice.add_vote')
@csrf.csrf_exempt
def report(request, voice_id):
    pass

@login_required
def show(request, voice_id):
    # Make sure that only original voices are shown using this view,
    # not sub-voices.
    voice = get_object_or_404(Voice, pk=voice_id, parent__isnull=True)

    # In case the voice is deleted or pending revision, only show it
    # to those with view_voice permission.
    if not voice.is_published and \
       not request.user.has_perm('studentvoice.view_voice'):
        raise Http404

    if request.user.has_perm('studentvoice.view_voice'):
        comments = voice.replies.filter(is_published__in=[True, None])
    else:
        comments = voice.replies.filter(is_published=True)
    view = View.objects.filter(viewer=request.user, voice=voice)
    if not view:
        View.objects.create(viewer=request.user, voice=voice)
        voice.update_views()
    context = {'voice': voice, 'comments': comments, 'message':
               request.GET.get('message')}
    if voice.is_editable and voice.is_published:
        context['comment_form'] = CommentForm()

    return render(request, 'studentvoice/show.html', context)

@login_required
@decorators.post_only
def create_comment(request, voice_id):
    # Don't make it possible to comment on comments that are not
    # published.
    parent_voice = get_object_or_404(Voice, pk=voice_id,
                                     is_published=True)
    greatest_parent = parent_voice.get_greatest_parent()
    comment_object = Voice(submitter=request.user,
                           parent=parent_voice)
    
    after_url = reverse('studentvoice:show', args=(greatest_parent.pk,))

    if not greatest_parent.is_published:
        after_url += "?message=deleted"
    elif not greatest_parent.is_editable:
        after_url += "?message=uneditable"
    else:
        form = CommentForm(request.POST, instance=comment_object)
        if form.is_valid():
            new_comment = form.save()
            greatest_parent.update_comments()
            after_url += '#comment-' + str(new_comment.pk)
        else:
            after_url += "?message=commenterror"
    return HttpResponseRedirect(after_url)

@login_required
def edit(request, voice_id):
    # Only edit those voices that are either published (True) or
    # pending revision (None).
    voice = get_object_or_404(Voice, pk=voice_id,
                                is_published__in=[True, None])
    greatest_parent = voice.get_greatest_parent()
    if greatest_parent == voice:
        is_comment = False
        Form = VoiceForm
    else:
        is_comment = True
        Form = CommentForm

    context = {'voice': voice, 'greatest_parent': greatest_parent,
               'edit': True, 'is_comment': is_comment}

    # If the user is the submitter of the voice, make sure that it is
    # editable and that is it in a thread that is editable.
    # Otherwise, if the user has change_voice, they can edit the voice
    # whatever its status is.
    if not (voice.submitter == request.user and \
       voice.is_editable and greatest_parent.is_editable) \
       and not request.user.has_perm('studentvoice.change_voice'):
        raise PermissionDenied

    if request.method == 'POST':
        form = Form(request.POST, instance=voice)
        if is_comment:
            after_url = reverse('studentvoice:show', args=(greatest_parent.pk,))+'#comment-' + voice_id
        else:
            after_url = reverse('studentvoice:show', args=(greatest_parent.pk,))
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(after_url)
        else:
            context['form'] = form
            return render(request, 'studentvoice/edit.html', context)
    elif request.method == 'GET':
        form = Form(instance=voice)
        context['form'] = form
        return render(request, 'studentvoice/edit.html', context)

@login_required
def delete(request, voice_id):
    # Only delete those voices that are either published (True) or
    # pending revision (None).
    voice = get_object_or_404(Voice, pk=voice_id,
                              is_published__in=[True, None])
    greatest_parent = voice.get_greatest_parent()

    # If the user is the submitter of the voice, make sure that it is
    # not already deleted (is_published=False) and that is editable.
    # Otherwise, if the user has delete_voice, they can delete the
    # voice whatever its status is (even though if it's already
    # deleted, nothing will change.)
    if greatest_parent.is_published == False or\
       not greatest_parent.is_editable:
        can_delete = False
    else:
        can_delete = True

    is_user_voice = request.user.voice_set.filter(id=voice_id)

    if not (is_user_voice and can_delete) and \
       not request.user.has_perm('studentvoice.delete_voice'):
        raise PermissionDenied

    if request.method == 'POST':
        if 'confirm' in request.POST:
            if voice != greatest_parent: # If it is a reply
                after_url = reverse('studentvoice:show',
                                args=(greatest_parent.pk,))
            else: # If it is the main voice
                after_url = reverse('studentvoice:home')
            voice.is_published = False
            voice.save()
            greatest_parent.update_comments()
            return HttpResponseRedirect(after_url)
        else:
            context = {'greatest_parent': greatest_parent, 'voice':
                       voice, 'error_message': 'not_confirmed'}
            return render(request, 'studentvoice/delete.html',
                          context)
    elif request.method == 'GET':
        context = {'greatest_parent': greatest_parent, 'voice': voice}
        return render(request, 'studentvoice/delete.html', context)

def create(request):
    if request.user.is_authenticated():
        template = 'studentvoice_base.html'
    else:
        template = 'front/front_base.html'

    if request.method == 'POST':
        if request.user.is_authenticated():
            voice_object = Voice(submitter=request.user)
        else:
            voice_object = Voice(is_published=False)
        form = VoiceForm(request.POST, instance=voice_object)
        if form.is_valid():
            new_voice = form.save()
            if request.user.is_authenticated():
                after_url = reverse('studentvoice:show',
                                    args=(new_voice.pk,))
            else:
                after_url = reverse('studentvoice:home'+'?message=submitted')
            return HttpResponseRedirect(after_url)
        else:
            context = {'form': form, 'template': template}
            return render(request, 'studentvoice/edit.html', context)
    elif request.method == 'GET':
        form = VoiceForm()
        context = {'form': form, 'template': template}
        return render(request, 'studentvoice/edit.html', context)

def search(request):
    if request.user.is_authenticated():
        template = 'studentvoice_base.html'
    else:
        template = 'front/front_base.html'
        
    if request.method == 'GET':
        context = {'page_voices': None}
        # Make sure that a query was submitted and that it isn't
        # empty.
        if 'q' in request.GET and request.GET['q']:
            context['q'] = request.GET['q']
            term = request.GET['q']
            if request.user.has_perm('voices.view_voices'):
                is_published = [True, None]
            else:
                is_published = [True]

            title_search = Voice.objects.filter(title__contains=term, is_published__in=is_published)
            text_search = Voice.objects.filter(text__contains=term, is_published__in=is_published)

            resulted_voices = title_search | text_search

            resulted_voices = resulted_voices.order_by('submission_date')

            parent_voices = []

            for voice in list(resulted_voices):
                greatest_parent = voice.get_greatest_parent()
                if greatest_parent in parent_voices:
                    continue
                else:
                    parent_voices.append(greatest_parent)

            context['total_results'] = len(parent_voices)

            # Each page of results should have a maximum of 25
            # activities.
            paginator = Paginator(parent_voices, 25)
            page = request.GET.get('page')

            try:
                page_voices = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                page_voices = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                page_voices = paginator.page(paginator.num_pages)
            context['page_voices'] = page_voices
        
        context['template'] = template
        return render(request, 'studentvoice/search.html', context)
