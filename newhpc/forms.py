from django.forms import ModelForm
from newhpc.models import FaqCategory, FaqQuestion, PreviousVersion, PreviousStatistics, HpcLeader, Winner, NewsletterMembership

class FaqCategoryForm(ModelForm):
    class Meta:
        model = FaqCategory
        fields = ['arabic_title','english_title']

class FaqQuestionForm(ModelForm):
    class Meta:
        model = FaqQuestion
        fields = ['category', 'is_tech', 'arabic_question',
                  'english_question', 'arabic_answer', 'english_answer']

class PreviousVersionForm(ModelForm):
    class Meta:
        model = PreviousVersion
        fields = ['arabic_title', 'english_title', 'arabic_vision', 'english_vision','logo']

class PreviousStatisticsForm(ModelForm):
    class Meta:
        model = PreviousStatistics
        fields = ['version','number_of_lectures','poster_presentations','number_of_winners',
                  'oral_presentations', 'number_of_workshops', 'number_of_speakers',
                  'number_of_abstracts', 'number_of_accepted_abstracts',
                  'number_of_universities', 'number_of_signs']

class HpcLeaderForm(ModelForm):
    class Meta:
        model = HpcLeader
        fields = ['version', 'arabic_name', 'image']


class WinnerForm(ModelForm):
    class Meta:
        model = Winner
        fields = ['version', 'arabic_name', 'presentation_type',
                  'rank','image']

class NewsletterMembershipForm(ModelForm):
    class Meta:
        model = NewsletterMembership
        fields = ['email']