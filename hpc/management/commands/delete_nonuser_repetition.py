from django.core.management.base import BaseCommand

from hpc.models import Registration


class Command(BaseCommand):
    help = "Delete repeated non-user repetitions."

    def handle(self, *args, **options):
        total_count = 0
        for registration in Registration.objects.filter(nonuser__isnull=False, is_deleted=False).order_by('-date_submitted').iterator():
            if not registration.is_deleted:
                continue
            email = registration.nonuser.email
            repetition = Registration.objects.filter(nonuser__email=email, is_deleted=False).exclude(pk=registration.pk)
            repetition.update(is_deleted=True)

            count = repetition.count()
            if count:
                total_count += count

            self.stdout.write(u'{} repetition for {}'.format(count, email))

        self.stdout.write("Total repetition: {}".format(total_count))
