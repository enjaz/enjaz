from contextlib import contextmanager
import os
import sys

from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.db.utils import OperationalError
from django.utils import timezone
from niqati.models import Code_Order


@contextmanager
def lockfile(path):
    if os.path.exists(path):
        print "Another procces is already running.  Abort this one."
        sys.exit(-1)
    else:
        open(path, 'w').write("1")
        try:
            yield
        except OperationalError: # Skip unexpected DB errors.
            pass
        finally:
            os.remove(path)

class Command(BaseCommand):
    help = 'Process approved niqati code orders'

    def handle(self, *args, **options):
        print timezone.now()

        # Since the currently used API does not support simultaneous
        # API, we need to ensure that if another proccess is already
        # running, it needs to be aborted.
        lockfile_path = os.getcwd() + '/niqati.lock'
        with localfile(lockfile_path):
            # Get all approved and unprocessed orders
            orders = filter(lambda order: order.is_approved() and order.is_processed() == False, Code_Order.objects.all())
            domain = Site.objects.get_current().domain
            submit_link = "http://" + domain + reverse('niqati:submit')
            for order in orders:
                if order.get_delivery_type() == '0':  # Coupon
                    # Check if the order is currently being processed; if so, abort
                    if not any([os.path.isfile('codes_' + str(collec.pk) + '.pdf') for collec in order.code_collection_set.all()]):
                        print "  Processing order number ", order.pk, " for the activity ", order.activity
                        try:
                            order.process(submit_link)
                            print "  ", timezone.now()
                            print "  Successfully generated requested coupons."
                        except:
                            order.mark_as_processed()
                            print "  ", timezone.now()
                            print "  Generation failed; marking order as complete and proceeding"
                    else: # TODO: With the lockfile, this condition seems to be redundant.
                        print "  Order currently being processed."
                        print "  Aborting..."
                elif order.get_delivery_type() == '1':  # Short links
                    # Check if the order is currently being processed; if so, abort
                    if not any([os.path.isfile('links_' + str(collec.pk) + '.html') for collec in order.code_collection_set.all()]):
                        print "  Order not currently being processed."
                        print "  Processing order number ", order.pk, " for the activity ", order.activity
                        try:
                            order.process(submit_link)
                            print "  ", timezone.now()
                            print "  Successfully generated requested short links."
                        except:
                            # FIXME: such an unspecific 'except' should
                            # never, ever be used.
                            order.mark_as_processed()
                            print "  ", timezone.now()
                            print "  Generation failed; marking order as complete and proceeding"
                    else: # TODO: With the lockfile, this condition seems to be redundant.
                        print "  Order currently being processed."
                        print "  Aborting..."
