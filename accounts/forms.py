from django import forms
from .models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField 

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email','phone_number', 'full_name')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(help_text = "you can change password in <a hrf \" ../password/\">this form</a>")
    class Meta:
        model = User
        fields = ('email','phone_number', 'full_name', 'is_active', 'is_admin')


class RegistrationForm(forms.Form):
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=11)
    full_name = forms.CharField(label= 'full name')
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('this email already exisit')
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        user = User.objects.filter(phone_number='phone_number').exists()
        if user:
            raise ValidationError('this email already exist')
        return phone_number

class VerfyCodeForm(forms.Form):
    code = forms.IntegerField()


class LoginUserForm(forms.Form):
    phone_number = forms.CharField(max_length=11)
    password = forms.CharField(widget=forms.PasswordInput)

