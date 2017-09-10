from django.shortcuts import redirect
from django.views import generic
from approvals.forms import ActivityCreateRequestForm, EventRequestFormSet, ActivityRequestResponseForm
from approvals.models import ActivityRequest, ActivityRequestReview


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
            return redirect("/")

        return self.render_to_response(self.get_context_data().update({
            'activity_request_form': activity_request_form,
            'event_request_formset': event_request_formset,
        }))


class ActivityRequestList(generic.TemplateView):
    template_name = "approvals/activityrequest_list.html"

    def get_context_data(self, **kwargs):
        return super(ActivityRequestList, self).get_context_data(**kwargs).update({
            'active_requests': ActivityRequest.objects.all(),
            'inactive_requests': ActivityRequest.objects.all(),
        })


class ActivityRequestDetail(generic.DetailView):
    model = ActivityRequest
    queryset = ActivityRequest.objects.all()
    template_name = "approvals/activityrequest_detail.html"
    context_object_name = "activity_request"


class ActivityApproval(generic.CreateView):
    model = ActivityRequestReview
    form_class = ActivityRequestResponseForm
