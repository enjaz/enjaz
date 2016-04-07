from django.core.management.base import BaseCommand

from events.models import Registration, Session


class Command(BaseCommand):
    help = "Delete repeated non-user repetitions."

    def handle(self, *args, **options):
        total_count = 0
        deleted = []
        for registration in Registration.objects.filter(nonuser__isnull=False, is_deleted=False).order_by('-date_submitted').iterator():
            if registration.is_deleted or registration.pk in deleted:
                continue

            sessions = Session.objects.none()

            email = registration.nonuser.email
            repetitions = Registration.objects.filter(nonuser__email=email, is_deleted=False).exclude(pk=registration.pk)
            count = repetitions.count()
            if count:
                for repetition in repetitions:
                    for session in repetition.first_priority_sessions.all():
                        if session.time_slot and registration.first_priority_sessions.filter(time_slot=session.time_slot).exists():
                            print "Conflict between {} and {}!".format(repetition.pk, registration.pk)
                        elif registration.first_priority_sessions.filter(pk=session.pk).exists():
                            print "I found {} repeated in both {} and {}.".format(session.pk, repetition.pk, registration.pk)
                        else:
                            continue
                        repetition.is_deleted = True
                        repetition.save()
                        deleted.append(repetition.pk)
                        print "Marked {} as deleted.".format(repetition.pk)
                        break
                    for session in repetition.second_priority_sessions.all():
                        if session.time_slot and registration.second_priority_sessions.filter(time_slot=session.time_slot).exists():
                            print "Conflict between {} and {}!".format(repetition.pk, registration.pk)
                        elif registration.second_priority_sessions.filter(pk=session.pk).exists():
                            print "I found {} repeated in both {} and {}.".format(session.pk, repetition.pk, registration.pk)
                        else:
                            continue
                        repetition.is_deleted = True
                        repetition.save()
                        deleted.append(repetition.pk)
                        print "Marked {} as deleted.".format(repetition.pk)
                        break

                total_count += count
            else:
                continue

            self.stdout.write(u'{} repetitions for {}'.format(count, email))

        self.stdout.write("Total repetitions: {}".format(total_count))
