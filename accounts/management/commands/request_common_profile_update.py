from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand
from django.core.urlresolvers import reverse

from post_office import mail


class Command(BaseCommand):
    help = "Notify users to update."

    def handle(self, *args, **options):
        domain = Site.objects.get_current().domain
        full_url = "https://{}{}".format(domain,
                                         reverse('edit_common_profile'))
        for user in User.objects.filter(common_profile__is_student=True,
                                        is_active=True):
            mail.send([user.email],
                       template="update_common_profile",
                       context={'user': user, 'full_url': full_url})
            self.stdout.write(u'Emailed {}.'.format(user.email))
