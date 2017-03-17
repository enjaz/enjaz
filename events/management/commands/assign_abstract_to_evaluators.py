from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from django.utils import translation, timezone
from django.contrib.auth.models import User
from events.models import Event,Abstract
from clubs.models import Team
from django.db.models import Count


class Command(BaseCommand):
    help = "Assign abstract to evaluators"
    def add_arguments(self, parser):
        parser.add_argument('--event-code-name', dest='event_code_name',
                            default=None, type=str)

    def handle(self, *args, **options):
        if not options['event_code_name']:
            print "No event code name was provided."
            return

        event= Event.objects.get(code_name=options['event_code_name'])

        if not event.abstract_revision_team:
            print "Event has no abstract revision team."
            return

        abstracrs_count = Abstract.objects.filter(event=event).count()
        evaluatin_team_members_count = Team.objects.get(code_name=event.abstract_revision_team).members.count()

        target_count = int(abstracrs_count/evaluatin_team_members_count)
        avalabile_members= Team.objects.get(code_name=event.abstract_revision_team).members.annotate(num_b=Count('abstract')).filter(num_b__lt=target_count)

        unassigned_abstracts = Abstract.objects.annotate(num_b=Count('evaluators')).filter(event=event, is_deleted=False,num_b__lt=2)
        for abstract in unassigned_abstracts:
            for member in avalabile_members:
                if member not in abstract.evaluators.all():
                    abstract.evaluators.add(member)
                    abstract.save()
