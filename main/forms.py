from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
)
from .models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate


class SignUpForm(UserCreationForm):
    password1 = forms.CharField(
        label="비밀번호",
        strip=False,
        widget=forms.PasswordInput(render_value=True),
        help_text="8~25글자 사이의 비밀번호를 입력해주세요",
    )
    password2 = forms.CharField(
        label="비밀번호 확인",
        strip=False,
        widget=forms.PasswordInput(render_value=True),
        help_text='비밀번호를 재입력해주세요',
    )

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2', 'nickname']
        labels = {
            'email': _('이메일'),
            'nickname': _('닉네임'),
        }
        help_texts = {
            'email': _('사용하실 이메일을 입력해주세요'),
            'nickname': _('10자 이내의 닉네임을 입력해주세요'),
        }


class SignInForm(forms.Form):
    error_messages = {
        'user_missmatch': _('이메일 혹은 비밀번호를 다시 입력해주세요')
    }
    email = forms.EmailField(
        label=_("이름"),
        widget=forms.EmailInput()
    )
    password = forms.CharField(
        label=_("비밀번호"),
        strip=False,
        widget=forms.PasswordInput(render_value=True),
    )

    class Meta:
        model = User
        fields = ['email']

    def __init__(self, *args, **kwargs):
        super(SignInForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget = forms.EmailInput(attrs={'placeholder': '이메일'})
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget = forms.PasswordInput(attrs={'placeholder': '비밀번호'})
        self.fields['password'].widget.attrs['class'] = 'form-control'

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        if user is None:
            raise forms.ValidationError(
                self.error_messages['user_missmatch'],
                code='user_missmatch',
            )
        return self.cleaned_data

    def get_user(self):
        return self.user


class UpdateUserInfoForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ['nickname', 'image', 'content']
        labels = {
            'nickname': _('닉네임'),
            'image': _('프로필 이미지'),
            'content': _('소개글'),
        }


class CheckPasswordForm(forms.Form):
    password = forms.CharField(
        label='비밀번호',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', }
        ),

    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = self.user.password

        if password:
            if not check_password(password, confirm_password):
                self.add_error('password', '비밀번호가 일치하지 않습니다.')


