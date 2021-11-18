from django import forms
from .models import CourseItem, Course
from django.utils.translation import gettext_lazy as _


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'thumbnail_image', 'user', ]
        labels = {
            'title': _('제목'),
            'thumbnail_image': _('썸네일 이미지'),
        }
        widgets = {
            'user': forms.HiddenInput(),
        }


class CourseItemForm(forms.ModelForm):
    class Meta:
        model = CourseItem
        fields = ['course', 'image', 'comment']
        labels = {
            'course': _('코스'),
            'image': _('이미지'),
            'comment': _('코멘트'),
        }
        widgets = {
            # 'course': forms.HiddenInput(),
            'user': forms.HiddenInput(),
        }
