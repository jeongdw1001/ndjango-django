from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django import forms
from django.contrib.auth import authenticate

# 회원가입 폼
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='이메일은 필수 입력값 입니다.')

    class Meta:
        model = CustomUser
        fields = ["email", "nickname", "password1", "password2"]

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = CustomUser.objects.get(email=email)
        except Exception as e:
            return email
        raise forms.ValidationError(f"{email}은 이미 존재하는 이메일입니다.")
 
    def clean_nickname(self):
        nickname = self.cleaned_data['nickname']
        try:
            account = CustomUser.objects.get(nickname=nickname)
        except Exception as e:
            return nickname
        raise forms.ValidationError(f"{nickname}은 이미 존재하는 닉네임입니다..")



# 로그인 인증 폼
class AccountAuthForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
 
    class Meta:
        model = CustomUser
        fields = ('email', 'password')
 
    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid login")        
 

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("email", "nickname", "age", "diet", "allergy")
        