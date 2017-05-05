# -*- coding: utf-8  -*-
from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.utils import translation
from openpyxl import load_workbook

from certificates.models import Certificate
from events.models import Abstract
from post_office import mail


class Command(BaseCommand):
    help = "Send badges emails."
    def add_arguments(self, parser):
        parser.add_argument('--excel-file', dest='excel_file',
                            type=str)
        parser.add_argument('--send-emails', dest='send_emails',
                            action='store_true', default=False)

    def handle(self, *args, **options):
        translation.activate(settings.LANGUAGE_CODE)
        wb = load_workbook(options['excel_file'], read_only=True)
        domain = Site.objects.get_current().domain
        from_email = event.get_notification_email()
        url = "https://{}{}".format(domain,
                                    reverse('certificates:list_certificates_per_user'))
        generated_pks = Certificate.objects.values_list('abstracts__pk', flat=True)

        for sheet_name in wb.get_sheet_names():
            sheet = wb[sheet_name]
            print "Reading sheet '{}'".format(sheet_name)
            for row in sheet:
                pk = row[0].value
                # If pk is empty, we are done from this sheet.
                if not pk:
                    break 
                try:
                    pk = int(pk)
                except ValueError:
                    # If pk cannot be turned into intger
                    # (i.e. header), skip!
                    continue

                if pk in previous_pks:
                    print "Skipping {} as previously generated.".format(pk)
                    continue

                authors = [cell.value.strip() for cell in row[3:12] if cell.value]
                abstract = Abstract.objects.get(pk=pk)

                # Let's make sure that the abstract deserves a
                # certificate
                if abstract.accepted_presentaion_preference in ['O', 'P'] and \
                   abstract.did_presenter_attend:
                    if abstract.accepted_presentaion_preference == 'O':
                        template = abstract.event.oral_certificate_template
                    elif abstract.accepted_presentaion_preference == 'P':
                        template = abstract.event.poster_certificate_template

                    for author in authors:
                        description = "شهادة {} لتقديم {}".format(author, abstract.title)
                        print 'Generating {}\'s "{}"'.format(author, abstract.title)
                        template.generate_certificate(user=abstract.user,
                                                      texts=[author, abstract.title],
                                                      description=description,
                                                      content_object=abstract)
                        # Other than the first author, we are going to
                        # use the co_author certificate template
                        template = abstract.event.coauthor_certificate_template
                    if options['send_emails']:
                        contxt = {'title': abstract.title,
                                  'user': abstract.user,
                                  'event': event,
                                  'url': url}
                        mail.send(abstract.email, from_email,
                                  template='event_abstract_certificate',
                                  context=context)
