import json
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.utils.http import urlquote
from email_extras.utils import send_mail_template
from forms_builder.forms.signals import form_invalid, form_valid
from future.builtins import bytes

from csv import writer
from datetime import datetime
from io import StringIO, BytesIO
from mimetypes import guess_type
from os.path import join

from django.contrib.contenttypes.models import ContentType
from django.core.files.storage import FileSystemStorage
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.utils.translation import ungettext, ugettext_lazy as _
from django.views.generic import TemplateView

from forms_builder.forms.settings import CSV_DELIMITER, UPLOAD_ROOT, EMAIL_FAIL_SILENTLY
from forms_builder.forms.forms import EntriesForm, FormForForm
from forms_builder.forms.models import Form, FormEntry, FieldEntry
from forms_builder.forms.utils import now, slugify, split_choices
from forms_builder.wrapper.forms import FormToBuildForm, FieldFormSet
from forms_builder.wrapper import settings as wrapper_settings

try:
    import xlwt
    XLWT_INSTALLED = True
    XLWT_DATETIME_STYLE = xlwt.easyxf(num_format_str='MM/DD/YYYY HH:MM:SS')
except ImportError:
    XLWT_INSTALLED = False

fs = FileSystemStorage(location=UPLOAD_ROOT)


class FormDetail(TemplateView):

    template_name = "forms/form_detail.html"

    def get_context_data(self, content_type=None, object_id=None, **kwargs):
        context = super(FormDetail, self).get_context_data(**kwargs)
        self.object = get_object_or_404(content_type.model_class(), id=object_id) if content_type is not None else None
        published = Form.objects.published(for_user=self.request.user, for_object=self.object,
                                           editor_check=kwargs.get("edit_perm_check"))
        kw = {"slug": kwargs["slug"]} if wrapper_settings.USE_SLUGS else {"id": kwargs["form_id"]}
        context["form"] = get_object_or_404(published,
                                            content_type=content_type, object_id=object_id,
                                            **kw)
        context["object_id"] = object_id
        context[kwargs.pop("object_context_name", "object")] = self.object
        context.update(kwargs.pop("custom_context", {}))
        return context

    def get(self, request, form_detail_template="forms/form_detail.html",
            *args, **kwargs):
        context = self.get_context_data(**kwargs)
        login_required = context["form"].login_required
        if login_required and not request.user.is_authenticated():
            path = urlquote(request.get_full_path())
            bits = (settings.LOGIN_URL, REDIRECT_FIELD_NAME, path)
            return redirect("%s?%s=%s" % bits)
        self.template_name = form_detail_template
        return self.render_to_response(context)

    def post(self, request, content_type=None, object_id=None,
             form_detail_template="forms/form_detail.html",
             *args, **kwargs):
        self.object = get_object_or_404(content_type.model_class(), id=object_id) if content_type is not None else None
        published = Form.objects.published(for_user=request.user, for_object=self.object,
                                           editor_check=kwargs.get("edit_perm_check"))
        kw = {"slug": kwargs["slug"]} if wrapper_settings.USE_SLUGS else {"id": kwargs["form_id"]}
        form = get_object_or_404(published,
                                 content_type=content_type, object_id=object_id,
                                 **kw)
        form_for_form = FormForForm(form, RequestContext(request),
                                    request.POST or None,
                                    request.FILES or None,
                                    instance=FormEntry(submitter=request.user
                                    if request.user.is_authenticated() else None))
        if not form_for_form.is_valid():
            form_invalid.send(sender=request, form=form_for_form)
        else:
            # Attachments read must occur before model save,
            # or seek() will fail on large uploads.
            attachments = []
            for f in form_for_form.files.values():
                f.seek(0)
                attachments.append((f.name, f.read()))
            entry = form_for_form.save()
            form_valid.send(sender=request, form=form_for_form, entry=entry)
            self.send_emails(request, form_for_form, form, entry, attachments)
            if not self.request.is_ajax():
                key = "slug" if wrapper_settings.USE_SLUGS else "form_id"
                return redirect(form.redirect_url or
                    reverse("forms:form_sent", current_app=request.resolver_match.namespace,
                            kwargs={key: form.get_url_attr(), "object_id": object_id}))
        context = {"form": form, "form_for_form": form_for_form, "object_id": object_id}
        context[kwargs.pop("object_context_name", "object")] = self.object
        context.update(kwargs.pop("custom_context", {}))
        self.template_name = form_detail_template
        return self.render_to_response(context)

    def render_to_response(self, context, **kwargs):
        if self.request.is_ajax():
            json_context = json.dumps({
                "errors": context["form_for_form"].errors,
                "form": context["form_for_form"].as_p(),
                "message": context["form"].response,
            })
            return HttpResponse(json_context, content_type="application/json")
        return super(FormDetail, self).render_to_response(context, current_app=self.request.resolver_match.namespace, **kwargs)

    def send_emails(self, request, form_for_form, form, entry, attachments):
        subject = form.email_subject
        if not subject:
            subject = "%s - %s" % (form.title, entry.entry_time)
        fields = []
        for (k, v) in form_for_form.fields.items():
            value = form_for_form.cleaned_data[k]
            if isinstance(value, list):
                value = ", ".join([i.strip() for i in value])
            fields.append((v.label, value))
        context = {
            "fields": fields,
            "message": form.email_message,
            "request": request,
        }
        email_from = form.email_from or settings.DEFAULT_FROM_EMAIL
        email_to = form_for_form.email_to()
        if email_to and form.send_email:
            send_mail_template(subject, "form_response", email_from,
                               email_to, context=context,
                               fail_silently=EMAIL_FAIL_SILENTLY)
        headers = None
        if email_to:
            headers = {"Reply-To": email_to}
        email_copies = split_choices(form.email_copies)
        if email_copies:
            send_mail_template(subject, "form_response_copies", email_from,
                               email_copies, context=context,
                               attachments=attachments,
                               fail_silently=EMAIL_FAIL_SILENTLY,
                               headers=headers)

form_detail = FormDetail.as_view()


def form_sent(request, content_type=None, object_id=None,
              form_sent_template="forms/form_sent.html", **kwargs):
    """
    Show the response message.
    """
    object = get_object_or_404(content_type.model_class(), id=object_id) if content_type is not None else None
    published = Form.objects.published(for_user=request.user, for_object=object,
                                       editor_check=kwargs.get("edit_perm_check"))
    kw = {"slug": kwargs["slug"]} if wrapper_settings.USE_SLUGS else {"id": kwargs["form_id"]}
    context = {"form": get_object_or_404(published, content_type=content_type, object_id=object_id, **kw),
               "object_id": object_id}
    context[kwargs.pop("object_context_name", "object")] = object
    context.update(kwargs.pop("custom_context", {}))
    template = form_sent_template
    return render_to_response(template, context, RequestContext(request, current_app=request.resolver_match.namespace))


def form_list(request, content_type=None, object_id=None,
              login_required_for_list=False,
              list_perm_check=lambda user, object: True,
              form_list_template="forms/form_list.html",
              form_list_edit_template="forms/form_list_edit.html",
              **kwargs):
    """
    Show the list of forms as appropriately specified.
    * If no arguments are passed, show all non-model-linked forms.
    * If a model instance is passed, show the models linked to that model instance (if any).
    """
    object = get_object_or_404(content_type.model_class(), id=object_id) if content_type is not None else None
    if login_required_for_list and not request.user.is_authenticated():
        path = urlquote(request.get_full_path())
        bits = (settings.LOGIN_URL, REDIRECT_FIELD_NAME, path)
        return redirect("%s?%s=%s" % bits)
    perm_check = list_perm_check
    # If user has edit permissions then user editor template; otherwise use normal template
    if request.user.is_authenticated() and perm_check(request.user, object):
        forms = Form.objects.filter(content_type=content_type, object_id=object_id)
        template = form_list_edit_template
    else:
        forms = Form.objects.published(for_user=request.user, for_object=object,
                                       editor_check=list_perm_check).filter(content_type=content_type, object_id=object_id)
        template = form_list_template
    context = {"forms": forms.annotate(total_entries=Count("entries")), "object_id": object_id}
    context[kwargs.pop("object_context_name", "object")] = object
    context.update(kwargs.pop("custom_context", {}))
    return render_to_response(template, context, RequestContext(request, current_app=request.resolver_match.namespace))


@login_required
def create_form(request, content_type=None, object_id=None,
                create_perm_check=lambda user, object: True,
                edit_form_template="forms/form_edit.html", **kwargs):
    """
    Create a form.
    The form can be either model-linked or not depending on the arguments passed.
    """
    object = get_object_or_404(content_type.model_class(), id=object_id) if content_type is not None else None
    perm_check = create_perm_check
    if perm_check(request.user, object) is False:
        raise PermissionDenied
    instance = Form(content_type=content_type, object_id=object_id)
    if request.method == 'POST':
        builder_form = FormToBuildForm(request.POST, instance=instance)
        formset = FieldFormSet(request.POST, instance=instance)
        if builder_form.is_valid() and formset.is_valid():
            form = builder_form.save()
            formset.instance = form
            formset.save()
            return HttpResponseRedirect(reverse('forms:form_list', current_app=request.resolver_match.namespace,
                                                kwargs={"object_id": object_id}))
    else:
        builder_form = FormToBuildForm()
        formset = FieldFormSet()
    template = edit_form_template
    context = {"builder_form": builder_form, "formset": formset, "object_id": object_id}
    context[kwargs.pop("object_context_name", "object")] = object
    context.update(kwargs.pop("custom_context", {}))
    return render_to_response(template, context,
                              RequestContext(request, current_app=request.resolver_match.namespace))


@login_required
def edit_form(request, form_id, content_type=None, object_id=None,
              edit_perm_check=lambda user, object: True,
              edit_form_template="forms/form_edit.html", **kwargs):
    """
    Edit an existing form.
    """
    object = get_object_or_404(content_type.model_class(), id=object_id) if content_type is not None else None
    perm_check = edit_perm_check
    if perm_check(request.user, object) is False:
        raise PermissionDenied
    form = get_object_or_404(Form, content_type=content_type, object_id=object_id, id=form_id)
    if request.method == 'POST':
        builder_form = FormToBuildForm(request.POST, instance=form)
        formset = FieldFormSet(request.POST, instance=form)
        if builder_form.is_valid() and formset.is_valid():
            builder_form.save()
            formset.save()
            return HttpResponseRedirect(reverse('forms:form_list', current_app=request.resolver_match.namespace,
                                                kwargs={"object_id": object_id}))
    else:
        builder_form = FormToBuildForm(instance=form)
        formset = FieldFormSet(instance=form)
    template = edit_form_template
    context = {"builder_form": builder_form, "formset": formset, "object_id": object_id}
    context[kwargs.pop("object_context_name", "object")] = object
    context.update(kwargs.pop("custom_context", {}))
    return render_to_response(template, context,
                              RequestContext(request, current_app=request.resolver_match.namespace))


@login_required
def delete_form(request, form_id, content_type=None, object_id=None,
                delete_perm_check=lambda user, object: True,
                delete_form_template="forms/form_delete.html", **kwargs):
    """
    Show a confirmation message for deletion.
    Delete form if confirmed.
    """
    object = get_object_or_404(content_type.model_class(), id=object_id) if content_type is not None else None
    perm_check = delete_perm_check
    if perm_check(request.user, object) is False:
        raise PermissionDenied
    form = get_object_or_404(Form, content_type=content_type, object_id=object_id, id=form_id)
    template = delete_form_template
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == "delete":
            form.delete()
            return HttpResponseRedirect(reverse('forms:form_list', current_app=request.resolver_match.namespace,
                                                kwargs={"object_id": object_id}))
        else:
            return HttpResponseRedirect(reverse('forms:edit_form', current_app=request.resolver_match.namespace,
                                                kwargs={"object_id": object_id, "form_id": form_id}))
    else:
        context = {"form": form, "object_id": object_id}
        context[kwargs.pop("object_context_name", "object")] = object
        context.update(kwargs.pop("custom_context", {}))
        return render_to_response(template, context,
                                  RequestContext(request, current_app=request.resolver_match.namespace))


@login_required
def entries_view(request, form_id, show=False, export=False,
                 export_xls=False, content_type=None, object_id=None,
                 entries_perm_check=lambda user, object: True,
                 submitter_fields=('user.username', ),
                 entries_template="forms/form_entries.html", **kwargs):
    """
    Displays the form entries.
    """
    model = Form
    template = entries_template
    formentry_model = FormEntry
    fieldentry_model = FieldEntry
    if request.POST.get("back"):
        #bits = (model._meta.app_label, model.__name__.lower())
        change_url = reverse("forms:edit_form", current_app=request.resolver_match.namespace,
                             kwargs={"object_id": object_id, "form_id": form_id})
        return HttpResponseRedirect(change_url)
    object = get_object_or_404(content_type.model_class(), id=object_id) if content_type is not None else None
    perm_check = entries_perm_check
    if perm_check(request.user, object) is False:
        raise PermissionDenied
    form = get_object_or_404(Form, content_type=content_type, object_id=object_id, id=form_id)
    post = request.POST or None
    args = form, request, formentry_model, fieldentry_model, post
    kw = {"submitter_fields": submitter_fields}
    entries_form = EntriesForm(*args, **kw)
    delete = "%s.delete_formentry" % formentry_model._meta.app_label
    can_delete_entries = request.user.has_perm(delete) # TODO: change to be based on delete_perm_check (at least add it)
    submitted = entries_form.is_valid() or show or export or export_xls
    export = export or request.POST.get("export")
    export_xls = export_xls or request.POST.get("export_xls")
    if submitted:
        if export:
            response = HttpResponse(mimetype="text/csv")
            fname = "%s-%s.csv" % (form.slug, slugify(now().ctime()))
            attachment = "attachment; filename=%s" % fname
            response["Content-Disposition"] = attachment
            queue = StringIO()
            try:
                csv = writer(queue, delimiter=CSV_DELIMITER)
                writerow = csv.writerow
            except TypeError:
                queue = BytesIO()
                delimiter = bytes(CSV_DELIMITER, encoding="utf-8")
                csv = writer(queue, delimiter=delimiter)
                writerow = lambda row: csv.writerow([c.encode("utf-8")
                    if hasattr(c, "encode") else c for c in row])
            writerow(entries_form.columns())
            for row in entries_form.rows(csv=True):
                writerow(row)
            data = queue.getvalue()
            response.write(data)
            return response
        elif XLWT_INSTALLED and export_xls:
            response = HttpResponse(mimetype="application/vnd.ms-excel")
            fname = "%s-%s.xls" % (form.slug, slugify(now().ctime()))
            attachment = "attachment; filename=%s" % fname
            response["Content-Disposition"] = attachment
            queue = BytesIO()
            workbook = xlwt.Workbook(encoding='utf8')
            sheet = workbook.add_sheet(form.title[:31])
            for c, col in enumerate(entries_form.columns()):
                sheet.write(0, c, col)
            for r, row in enumerate(entries_form.rows(csv=True)):
                for c, item in enumerate(row):
                    if isinstance(item, datetime):
                        item = item.replace(tzinfo=None)
                        sheet.write(r + 2, c, item, XLWT_DATETIME_STYLE)
                    else:
                        sheet.write(r + 2, c, item)
            workbook.save(queue)
            data = queue.getvalue()
            response.write(data)
            return response
        elif request.POST.get("delete") and can_delete_entries:
            selected = request.POST.getlist("selected")
            if selected:
                try:
                    from django.contrib.messages import info
                except ImportError:
                    def info(request, message, fail_silently=True):
                        request.user.message_set.create(message=message)
                entries = formentry_model.objects.filter(id__in=selected)
                count = entries.count()
                if count > 0:
                    entries.delete()
                    message = ungettext("1 entry deleted",
                                        "%(count)s entries deleted", count)
                    info(request, message % {"count": count})
    context = {"title": _("View Entries"), "entries_form": entries_form,
               "opts": model._meta, "original": form,
               "can_delete_entries": can_delete_entries,
               "submitted": submitted,
               "xlwt_installed": XLWT_INSTALLED,
               "object_id": object_id}
    context[kwargs.pop("object_context_name", "object")] = object
    context.update(kwargs.pop("custom_context", {}))
    return render_to_response(template, context, RequestContext(request, current_app=request.resolver_match.namespace))


@login_required
def file_view(request, field_entry_id,
              file_perm_check=lambda user, object: True,
              content_type=None, object_id=None, **kwargs):
    """
    Output the file for the requested field entry.
    """
    fieldentry_model = FieldEntry
    object = get_object_or_404(content_type.model_class(), id=object_id) if content_type is not None else None
    field_entry = get_object_or_404(fieldentry_model, entry__form__content_type=content_type,
                                    entry__form__object_id=object_id, id=field_entry_id)
    perm_check = file_perm_check
    if perm_check(request.user, object) is False:
        raise PermissionDenied
    path = join(fs.location, field_entry.value)
    response = HttpResponse(mimetype=guess_type(path)[0])
    f = open(path, "r+b")
    response["Content-Disposition"] = "attachment; filename=%s" % f.name
    response.write(f.read())
    f.close()
    return response