from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http.response import Http404
from django.shortcuts import redirect
from django.views import generic
from approvals.forms import ActivityCreateRequestForm, EventRequestFormSet, ActivityRequestResponseForm
from approvals.models import ActivityRequest, ActivityRequestReview, RequestThreadManager


class SubmitActivityCreateRequest(generic.TemplateView):
    template_name = "approvals/submit_activity_creation_request.html"

    def get_context_data(self, **kwargs):
        context = super(SubmitActivityCreateRequest, self).get_context_data(**kwargs)
        context.update({
            'activity_request_form': ActivityCreateRequestForm,
            'event_request_formset': EventRequestFormSet,
        })
        return context

    def post(self, request, *args, **kwargs):
        activity_request_form = ActivityCreateRequestForm(self.request.POST, instance=ActivityRequest())
        event_request_formset = EventRequestFormSet(self.request.POST, instance=activity_request_form.instance)

        if activity_request_form.is_valid() and event_request_formset.is_valid():
            activity_request_form.save()
            event_request_formset.save()
            return redirect(reverse("approvals:requestthread-list"))

        return self.render_to_response(self.get_context_data().update({
            'activity_request_form': activity_request_form,
            'event_request_formset': event_request_formset,
        }))


class RequestThreadList(generic.ListView):
    template_name = "approvals/requestthread_list.html"
    context_object_name = "request_threads"

    def get_queryset(self):
        return RequestThreadManager.all()


class RequestThreadDetail(generic.DetailView):
    template_name = "approvals/requestthread_detail.html"
    context_object_name = "request_thread"

    def get_object(self, queryset=None):
        try:
            return RequestThreadManager.get(id=self.kwargs.get(self.pk_url_kwarg))
        except ObjectDoesNotExist:
            raise Http404


class ActivityApproval(generic.CreateView):
    model = ActivityRequestReview
    form_class = ActivityRequestResponseForm
