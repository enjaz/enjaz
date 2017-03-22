from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db.models import Count
from django.utils import timezone
from events.models import Event, Abstract

import math


class Command(BaseCommand):
    help = "Assign abstract to evaluators"
    def add_arguments(self, parser):
        parser.add_argument('--event-code-name', dest='event_code_name',
                            default=None, type=str)

    def handle(self, *args, **options):
        if not options['event_code_name']:
            print "No event code name was provided."
            return

        event = Event.objects.get(code_name=options['event_code_name'])

        if not event.abstract_revision_team:
            print "Event has no abstract revision team."
            return

        abstract_count = Abstract.objects.filter(event=event, is_deleted=False).count()
        evaluatin_team_members_count = event.abstract_revision_team.members.count()
        target_abstracts_per_evaluator = float(abstract_count) * event.evaluators_per_abstract / evaluatin_team_members_count
        target_abstracts_per_evaluator = math.ceil(target_abstracts_per_evaluator)
        target_abstracts_per_evaluator = int(target_abstracts_per_evaluator)

        # Relieve over-worked evaluators
        overworked_evaluators = event.abstract_revision_team.members\
                                                            .annotate(abstract_count=Count('abstract'))\
                                                            .filter(abstract_count__gt=target_abstracts_per_evaluator)
        print "There are {} overworked evalautors:".format(overworked_evaluators.count())
        for evaluator in overworked_evaluators:
            print "* {} ({})".format(evaluator.username, evaluator.abstract_count)
            extra_abstract_count = evaluator.abstract_count - target_abstracts_per_evaluator
            extra_abstracts = evaluator.abstract_set.all()[:extra_abstract_count]
            for abstract in extra_abstracts:
                abstract.evaluators.remove(evaluator)

        unassigned_abstracts = Abstract.objects.annotate(evaluator_count=Count('evaluators'))\
                                               .filter(event=event, is_deleted=False,
                                                       evaluator_count__lt=event.evaluators_per_abstract)

        print "There are {} unassigned abstracts:".format(unassigned_abstracts.count())
        for abstract in unassigned_abstracts:
            remaining_evaluators = event.evaluators_per_abstract - abstract.evaluator_count
            for i in range(remaining_evaluators):
                evaluator_pks = abstract.evaluators.values_list("pk", flat=True)
                evaluator = event.abstract_revision_team.members\
                                                        .annotate(abstract_count=Count('abstract'))\
                                                        .filter(abstract_count__lt=target_abstracts_per_evaluator)\
                                                        .exclude(pk__in=evaluator_pks)\
                                                        .order_by("?")\
                                                        .first()
                if not evaluator:
                    print "No available evalautors!"
                    return
                abstract.evaluators.add(evaluator)
            print "* {} ({})".format(abstract.title, abstract.evaluators.count())
