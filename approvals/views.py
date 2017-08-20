from django.shortcuts import redirect
from django.views import generic
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from approvals.forms import ActivityCreateRequestForm, EventRequestFormSet
from approvals.models import ActivityRequest


class SubmitActivityCreateRequest(generic.TemplateView):
    template_name = "approvals/submit-activity-create-request.html"

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
class RequestDetail(DetailView):
    Model = ActivityRequest

    def get_context_data(self, pk, **kwargs):
        context = super(RequestDetail, self).get_context_data(**kwargs)
        context['show_request'] = get_object_or_404(Activity, pk=activity_id, is_deleted=False)
        return context

class ActivtyApproval(CreateView):
    model = ActivityRequsetResponseForm
    
