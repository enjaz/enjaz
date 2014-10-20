from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.utils import timezone
from niqati.models import Code_Order
import os

class Command(BaseCommand):
    help = 'Process approved niqati code orders'

    def handle(self, *args, **options):
        # Get all approved and unprocessed orders
        orders = filter(lambda order: order.is_approved() and order.is_processed() == False, Code_Order.objects.all())
        domain = Site.objects.get_current().domain
        submit_link = "http://" + domain + reverse('niqati:submit')
        for order in orders:
            print timezone.now()
            if order.get_delivery_type() == '0':  # Coupon
                # Check if the order is currently being processed; if so, abort
                if not any([os.path.isfile('codes_' + str(collec.pk) + '.pdf') for collec in order.code_collection_set.all()]):
                    print "  Order not currently being processed."
                    print "  Processing order number ", order.pk, " for the activity ", order.activity
                    try:
                        order.process(submit_link)
                        print "  ", timezone.now()
                        print "  Successfully generated requested coupons."
                    except:
                        order.mark_as_processed()
                        print "  ", timezone.now()
                        print "  Generation failed; marking order as complete and proceeding"
                else:
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
                else:
                    print "  Order currently being processed."
                    print "  Aborting..."
