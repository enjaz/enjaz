import os

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "studentportal.settings")

from django.core.urlresolvers import reverse
from django.conf import settings

from post_office import mail
from studentvoice.models import Voice

for voice in Voice.objects.filter(was_sent=False, parent__isnull=True,
                                  is_published=True,
                                  response__isnull=True,
                                  score__gte=settings.STUDENTVOICE_THRESHOLD):
    url = reverse('studentvoice:show', args=(voice.pk,))
    email_context = {'voice': voice, 'url': url}

    print "Handling voice #%d..." % voice.pk

    # Send notification to the voice recipient
    print "Preparing recipient email to %s..." % voice.recipient.email
    if voice.recipient.secondary_email:
        secondary_email = [voice.recipient.secondary_email]
        print "Adding secondary_email, as CC."
    else:
        secondary_email = None
    mail.send([voice.recipient.email], cc=secondary_email,
              template="studentvoice_threshold_recipient",
              context=email_context)
    # Send notification to the voice submitter
    print "Preparing submitter email to %s..." % voice.submitter.email
    mail.send([voice.submitter.email],
              template="studentvoice_threshold_submitter",
              context=email_context)
    # Send notification to the those who voted in favor of the voice
    for vote in voice.vote_set.filter(is_counted=True, vote_type='U'):
        print "Preparing voter email to %s..." % vote.submitter.email
        email_context['vote'] = vote
        mail.send([vote.submitter.email],
                  template="studentvoice_threshold_voter",
                  context=email_context)
    voice.was_sent = True
    voice.is_editable = False
    voice.save()
