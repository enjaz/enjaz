from django.forms import ModelForm
from newhpc.models import FaqCategory, FaqQuestion, PreviousVersion, PreviousStatistics, HpcLeader, MediaSponser, Winner

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
        fields = ['arabic_title', 'english_title', 'arabic_vision', 'english_vision']

class PreviousStatisticsForm(ModelForm):
    class Meta:
        model = PreviousStatistics
        fields = ['version', 'arabic_name', 'english_name',
                  'number_of_attendee', 'number_of_workshops', 'number_of_speakers',
                  'number_of_abstracts', 'number_of_accepted_abstracts',
                  'number_of_universities', 'number_of_signs']

class HpcLeaderForm(ModelForm):
    class Meta:
        model = HpcLeader
        fields = ['version', 'arabic_name', 'english_name', 'image']

class MediaSponserForm(ModelForm):
    class Meta:
        model = MediaSponser
        fields = ['version', 'arabic_name', 'english_name', 'logo']

class WinnerForm(ModelForm):
    class Meta:
        model = Winner
        fields = ['version', 'arabic_name', 'english_name',
                  'arabic_description', 'english_description', 'image']
