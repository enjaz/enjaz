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
        print timezone.now()
        # Process the orders one at a time so take only the first order
        if len(orders) > 0:
            order = orders.pop(0)

            domain = Site.objects.get_current().domain
            submit_link = "http://" + domain + reverse('niqati:submit')

            if order.get_delivery_type() == '0':  # Coupon
                # Check if no other coupons are already being generated at the moment
                if not os.path.isfile('codes.pdf'):
                    print "  No coupons currently being generated."
                    print "  Processing order number ", order.pk, " for the activity ", order.activity
                    order.process(submit_link)
                    print "  ", timezone.now()
                    print "  Successfully generated requested coupons."
                else:
                    print "  Other codes are currently being generated"
                    print "  Aborting..."
            elif order.get_delivery_type() == '1':  # Short links
                # Check if no other links are being generated
                if not os.path.isfile('links.html'):
                    print "  No other short links are being generated"
                    print "  Processing order number ", order.pk, " for the activity ", order.activity
                    order.process(submit_link)
                    print "  ", timezone.now()
                    print "  Successfully generated requested short links."
                else:
                    print "  Other short links are currently being generated."
                    print "  Aborting..."
        else:
            print "  No approved and unprocessed orders."