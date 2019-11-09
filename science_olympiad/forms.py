from django.forms import ModelForm
from .models import Inventor

class InventorForm(ModelForm):
    class Meta:
        model = Inventor
        fields = ['ar_name', 'en_name', 'job', 'workplace', 'invention_name',
                  'inv_category', 'other_category', 'summary', 'is_prototype', 'prototype_file']
