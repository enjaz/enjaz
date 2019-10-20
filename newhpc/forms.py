from django.forms import ModelForm
from newhpc.models import FaqCategory, FaqQuestion


class FaqCategoryForm(ModelForm):
    class Meta:
        model = FaqCategory
        fields = ['arabic_title','english_title']

class FaqQuestionForm(ModelForm):
    class Meta:
        model = FaqQuestion
        fields = ['category', 'is_tech', 'arabic_question',
                  'english_question', 'arabic_answer', 'english_answer']
