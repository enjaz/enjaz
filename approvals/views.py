from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse, reverse_lazy
from django.http.response import Http404
from django.shortcuts import redirect
from django.views import generic

from activities.models import Activity
from approvals.forms import ActivityCreateRequestForm, EventRequestFormSet, ActivityRequestResponseForm, \
    RequirementRequestFormSet, FileAttachmentFormSet, DepositoryItemRequestFormSet, ActivityRequestCommentForm, \
    ActivityRequestReviewForm
from approvals.models import ActivityRequest, ActivityRequestReview, RequestThreadManager, ActivityRequestComment


class SubmitActivityCreateRequest(generic.TemplateView):
    template_name = "approvals/submit_activity_creation_request.html"

    def get_context_data(self, **kwargs):
        context = super(SubmitActivityCreateRequest, self).get_context_data(**kwargs)
        context.update({
            'activity_request_form': ActivityCreateRequestForm,
            'event_request_formset': EventRequestFormSet,
            'depository_item_request_formset': DepositoryItemRequestFormSet,
            'requirement_request_formset': RequirementRequestFormSet,
            'file_attachment_formset': FileAttachmentFormSet,
        })
        return context

    def post(self, request, *args, **kwargs):
        activity_request_form = ActivityCreateRequestForm(self.request.POST, instance=ActivityRequest())
        event_request_formset = EventRequestFormSet(self.request.POST, instance=activity_request_form.instance)
        depository_item_request_formset = DepositoryItemRequestFormSet(self.request.POST, instance=activity_request_form.instance)
        requirement_request_formset = RequirementRequestFormSet(self.request.POST, instance=activity_request_form.instance)
        file_attachment_formset = FileAttachmentFormSet(self.request.POST, self.request.FILES, instance=activity_request_form.instance)

        if activity_request_form.is_valid() and event_request_formset.is_valid() \
                and depository_item_request_formset.is_valid() and requirement_request_formset.is_valid() \
                and file_attachment_formset.is_valid():
            activity_request_form.save()
            event_request_formset.save()
            depository_item_request_formset.save()
            requirement_request_formset.save()
            file_attachment_formset.save()
            return redirect(reverse("approvals:requestthread-list"))

        return self.render_to_response(self.get_context_data().update({
            'activity_request_form': activity_request_form,
            'event_request_formset': event_request_formset,
            'depository_item_request_formset': depository_item_request_formset,
            'requirement_request_formset': requirement_request_formset,
            'file_attachment_formset': file_attachment_formset,
        }))


class RequestThreadList(generic.TemplateView):
    template_name = "approvals/requestthread_list.html"

    def get_context_data(self, **kwargs):
        return {
            'active_request_threads': RequestThreadManager.filter(is_active=True),
            'inactive_request_threads': RequestThreadManager.filter(is_active=False),
        }


class RequestThreadDetail(generic.DetailView):
    template_name = "approvals/requestthread_detail.html"
    context_object_name = "request_thread"

    def get_object(self, queryset=None):
        try:
            return RequestThreadManager.get(id=self.kwargs.get(self.pk_url_kwarg))
        except ObjectDoesNotExist:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super(RequestThreadDetail, self).get_context_data(**kwargs)
        context.update({
            'comment_form': ActivityRequestCommentForm(),
            'review_form': ActivityRequestReviewForm(),
        })
        return context


class HandleActivityRequestCommentForm(generic.CreateView):
    form_class = ActivityRequestCommentForm
    template_name = "approvals/requestthread_list.html"  # This view only handles post requests; we shouldn't need this
    http_method_names = ['post']  # Is this the best way to specify we're only handling POST?

    def get_form_kwargs(self):
        """
        Automatically set the author and thread_id fields.
        """
        kwargs = super(HandleActivityRequestCommentForm, self).get_form_kwargs()
        kwargs.update({
            'instance': ActivityRequestComment(author=self.request.user, thread_id=self.kwargs.get('pk')),
        })
        return kwargs

    def get_success_url(self):
        return reverse('approvals:requestthread-detail', args=(self.kwargs.get('pk'), ))


class HandleActivityRequestReviewForm(generic.CreateView):
    form_class = ActivityRequestReviewForm
    template_name = "approvals/requestthread_list.html"
    http_method_names = ['post']

    def get_form_kwargs(self):
        kwargs = super(HandleActivityRequestReviewForm, self).get_form_kwargs()
        kwargs.update({
            'instance': ActivityRequestReview(
                request=RequestThreadManager.get(id=self.kwargs.get('pk')).requests.last(),
                submitter=self.request.user
            ),
        })
        return kwargs

    def form_valid(self, form):
        if form.cleaned_data.get('is_approved'):
            # Create Activity object and link it to original activity request
            activity_request = form.instance.request
            activity_request.activity = Activity.objects.create(
                team=activity_request.submitter_team,
                name=activity_request.name,
                description=activity_request.description,
                public_description=activity_request.description,
                goals=activity_request.goals,
                category=activity_request.category,
                gender=activity_request.gender,
                is_approved=True,
            )
            for event_request in activity_request.eventrequests.all():
                activity_request.activity.episode_set.create(
                    start_date=event_request.date,
                    end_date=event_request.date,
                    start_time=event_request.start_time,
                    end_time=event_request.end_time,
                    location=event_request.location,
                )
            activity_request.save()
        return super(HandleActivityRequestReviewForm, self).form_valid(form)

    def get_success_url(self):
        return reverse('approvals:requestthread-detail', args=(self.kwargs.get('pk'), ))


class ActivityApproval(generic.CreateView):
    model = ActivityRequestReview
    form_class = ActivityRequestResponseForm
