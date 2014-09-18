from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from niqati.models import Code_Order
import os

class Command(BaseCommand):
    help = 'Process approved niqati code orders'

    def handle(self, *args, **options):
        # Get all approved and unprocessed orders
        orders = filter(lambda order: order.is_approved() and order.is_processed() == False, Code_Order.objects.all())
        # Process the orders one at a time so take only the first order
        if len(orders) > 0:
            order = orders.pop(0)

            domain = Site.objects.get_current().domain
            submit_link = domain + reverse('niqati:submit')
            print domain
            print submit_link

            if order.get_delivery_type() == '0':  # Coupon
                # Check if no other coupons are already being generated at the moment
                if not os.path.isfile('codes.pdf'):
                    print "No codes being generated; proceeding..."

                    order.process(submit_link)
                else:
                    print "Other codes are currently being generated; aborting..."
            elif order.get_delivery_type() == '1':  # Short links
                # Check if no other links are being generated
                if not os.path.isfile('links.html'):
                    print "No other links are being generated; proceeding..."

                    order.process(submit_link)
                else:
                    print "Other links are currently being generated; aborting..."
        else:
            print "No approved and unprocessed orders"