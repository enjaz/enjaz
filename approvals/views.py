from django.shortcuts import redirect, render
from django.views import generic

from approvals.forms import ActivityCreateRequestForm, EventRequestFormSet
from approvals.models import ActivityRequest


class SubmitActivityCreateRequest(generic.detail.SingleObjectTemplateResponseMixin, generic.base.ContextMixin, generic.edit.ProcessFormView):
    template_name = "approvals/submit_activity_create_request.html"

    def get_context_data(self, **kwargs):
        context = super(SubmitActivityCreateRequest, self).get_context_data(**kwargs)
        context.update({
            'activity_request_form': ActivityCreateRequestForm,
            'event_request_formset': EventRequestFormSet,
        })
        return context

    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data())

    def post(self, **kwargs):
        activity_request_form = ActivityCreateRequestForm(self.request.POST, instance=ActivityRequest())
        event_request_formset = EventRequestFormSet(self.request.POST, instance=activity_request_form.instance)

        if activity_request_form.is_valid() and event_request_formset.is_valid():
            activity_request_form.save()
            event_request_formset.save()
            return redirect("/")

        return render(self.request, self.template_name, self.get_context_data().update({
            'activity_request_form': activity_request_form,
            'event_request_formset': event_request_formset,
        }))
