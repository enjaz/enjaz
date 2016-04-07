# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('niqati', '0010_attendee_direct_entry'),
    ]

    operations = [
        migrations.RenameModel("Code_Collection", "Collection"),
        migrations.RenameModel("Code_Order", "Order")
    ]
