from __future__ import unicode_literals
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
        parser.add_argument('--username', dest='username', default=None,
                            type=str)
        parser.add_argument('--number_of_abstracts_to_assign',
                            dest='number_of_abstracts_to_assign',default=None, type=int)

    def handle(self, *args, **options):
        if not options['event_code_name']:
            print "No event code name was provided."
            return
        if not options['username']:
            print "No username was provided."
            return
        if not options['number_of_abstracts_to_assign']:
            print "No number of abbstract to assign was provided."

        event = Event.objects.get(code_name=options['event_code_name'])
        new_evaluator = User.objects.filter(username=options['username']).first()
        number_of_abstracts_to_assign = int(options['number_of_abstracts_to_assign'])

        if not event.abstract_revision_team:
            print "Event has no abstract revision team."
            return

        if not new_evaluator:
            print "User doesn't exist."
            return

        print "Event name:", event.english_name
        print "Assigned user:", new_evaluator
        print "Number of abstracts assigned:", number_of_abstracts_to_assign

        pending_abstracts = Abstract.objects.annotate(num_b=Count('evaluation')).filter(event=event, is_deleted=False,
                                                                                        num_b__lt=event.evaluators_per_abstract)
        print "There are {} pending abstracts:".format(pending_abstracts.count())

        targeted_abstracts = pending_abstracts.exclude(evaluation__evaluator=new_evaluator)\
                                              .exclude(evaluators=new_evaluator)

        if number_of_abstracts_to_assign > targeted_abstracts.count():
            print "WARNING: There is not enough abstracts to assign!"

        for abstract in targeted_abstracts[:number_of_abstracts_to_assign]:
            pending_evaluator = abstract.evaluators.exclude(event_abstract_evaluations__abstract=abstract).first()
            if not pending_evaluator:
                continue
            abstract.evaluators.remove(pending_evaluator)
            abstract.evaluators.add(new_evaluator)
            print "Removed {} and aded {} from {}".format(pending_evaluator.username,
                                                          new_evaluator.username,
                                                          abstract.title)
