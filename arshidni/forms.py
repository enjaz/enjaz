# -*- coding: utf-8  -*-
from arshidni.models import GraduateProfile, Question, Answer, StudyGroup, LearningObjective, JoinStudyGroupRequest, ColleagueProfile, SupervisionRequest
from django import forms

class GraduateProfileForm(forms.ModelForm):
    class Meta:
        model = GraduateProfile
        fields = ['contacts', 'bio', 'interests',
                  'answers_questions', 'gives_lectures']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text']

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']

class StudyGroupForm(forms.ModelForm):
    class Meta:
        model = StudyGroup
        fields = ['name', 'starting_date', 'ending_date',
                  'max_members']

    def clean(self):
        cleaned_data = super(StudyGroupForm, self).clean()
        if 'starting_date' in cleaned_data and 'ending_date' in cleaned_data:
            if cleaned_data['starting_date'] > cleaned_data['ending_date']:
                msg = u'تاريخ انتهاء المدة قبل تاريخ بدئها!'
                self._errors["starting_date"] = self.error_class([msg])
                self._errors["ending_date"] = self.error_class([msg])
                # Remove invalid fields
                del cleaned_data["starting_date"]
                del cleaned_data["ending_date"]

        new_learningobjective_fields = [field for field in self.data if field.startswith('new_learningobjective-')]
        existing_learningobjective_fields = [field for field in self.data if field.startswith('existing_learningobjective-')]

        for field_name in new_learningobjective_fields:
            text = self.data[field_name].strip()
            if not text: # if empty
                continue
            cleaned_data[field_name] = self.data[field_name]
        for field_name in existing_learningobjective_fields:
            text = self.data[field_name].strip()
            if not text: # if empty
                continue
            cleaned_data[field_name] = self.data[field_name]

        return cleaned_data

    def clean_max_members(self):
        "Define max_members range."
        # TODO: Move this hard-coded number into a Django setting.
        # The maximum number of students in each group is 8.
        max_members = self.cleaned_data["max_members"]
        if max_members > 8:
            msg = u'لا يمكن أن يكون عدد أعضاء المجموعة أكثر من 8!'
            self._errors["max_members"] = self.error_class([msg])
        elif max_members < 3:
            msg = u'لا يمكن أن يكون عدد أعضاء المجموعة أقل من 3!'
            self._errors["max_members"] = self.error_class([msg])
        return max_members

    def save(self, *args, **kwargs):
        group = super(StudyGroupForm, self).save(*args, **kwargs)
        remaining_pk = [] # List of kept learning objects (whether
                          # modified or not)
        new_learningobjective_fields = [field for field in self.cleaned_data if field.startswith('new_learningobjective-')]
        existing_learningobjective_fields = [field for field in self.cleaned_data if field.startswith('existing_learningobjective-')]

        for field_name in new_learningobjective_fields:
            text = self.cleaned_data[field_name]
            new_learningobjective = LearningObjective.objects.create(group=group,text=text)
            remaining_pk.append(new_learningobjective.pk)

        for field_name in existing_learningobjective_fields:
            pk_str = field_name.lstrip("existing_learningobjective-")
            pk = int(pk_str)
            remaining_pk.append(pk)
            text = self.cleaned_data[field_name]
            existing_learningobjective = LearningObjective.objects.get(pk=pk)
            existing_learningobjective.text = text
            existing_learningobjective.save()

        deleted_learningobjectives = LearningObjective.objects.exclude(pk__in=remaining_pk).filter(group=group)
        for deleted_learningobjective in deleted_learningobjectives:
            print "Deleting", deleted_learningobjective.text
            deleted_learningobjective.delete()

        return group

class ColleagueProfileForm(forms.ModelForm):
    class Meta:
        model = ColleagueProfile
        fields = ['batch', 'contacts', 'bio', 'interests']

class SupervisionRequestForm(forms.ModelForm):
    class Meta:
        model = SupervisionRequest
        fields = ['batch', 'contacts', 'interests']
