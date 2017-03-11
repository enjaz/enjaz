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

    def handle(self, *args, **options):
        event= Event.objects.filter(code_name='hpc2-r')
        abstracrs_count = Abstract.objects.filter(event=event).count()
        evaluatin_team_members_count = Team.objects.get(code_name="hpc2-r-e").members.count()
        assigened_abstrsts_count = int(abstracrs_count/evaluatin_team_members_count)
        avalabile_members= Team.objects.get(code_name="hpc2-r-e").members.annotate(num_b=Count('abstract')).filter(num_b__lt=assigened_abstrsts_count)
        unassigned_abstracts = Abstract.objects.annotate(num_b=Count('evaluators')).filter(event=event, is_deleted=False,num_b__lt=2)
        for abstract in unassigned_abstracts:
            for member in avalabile_members:
                if member not in abstract.evaluators.all():
                    abstract.evaluators.add(member)
                    abstract.save()