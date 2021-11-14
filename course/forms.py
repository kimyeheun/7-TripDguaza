from django import forms
from .models import Course
from django.utils.translation import gettext_lazy as _


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['image', 'title', 'comment', 'user']
        labels = {
            'image': _('사진'),
            'title': _('제목'),
            'comment': _('코멘트'),
            # 'place': _('장소'),
        }
        widgets = {
            'user': forms.HiddenInput(),
            # 'place': forms.HiddenInput(),
        }
        help_texts = {
            'title': _('제목을 작성해주세요.'),
            'comment': _('코멘트를 작성해주세요.'),
        }


class CourseUpdateForm(CourseForm):
    class Meta:
        model = Course
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CourseForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(CourseForm, self).save(commit=False)

        if commit:
            instance.save()
        return instance
