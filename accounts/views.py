from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from .forms import RegistrationForm, VerfyCodeForm, LoginUserForm
from utils import send_otp_code
import random
from .models import OtpCode, User
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

class RegistrationView(View):
    form_class = RegistrationForm
    template_name = 'accounts/register.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form':form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            random_code = random.randint(1000, 9999)
            send_otp_code(form.cleaned_data['phone_number'], random_code)
            OtpCode.objects.create(phone_number=form.cleaned_data['phone_number'], code=random_code)
            request.session['user_register_info'] = {
                'phone_number': form.cleaned_data['phone_number'],
                'email': form.cleaned_data['email'],
                'full_name':form.cleaned_data['full_name'],
                'password':form.cleaned_data['password']
            }
            messages.success(request, 'we sent you a code', 'succsess')
            return redirect('accounts:verify_code')
        return render(request, self.template_name, {'form':form})


class UserRegisterVerifyCodeView(View):
    form_class = VerfyCodeForm

    def get(self, request):
        form = self.form_class
        return render(request, 'accounts/verify.html', {'form':form})    

    def post(self, request):
        user_session = request.session['user_register_info']
        code_instance = OtpCode.objects.get(phone_number= user_session['phone_number'])
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['code'] == code_instance.code:
                User.objects.create_user(user_session['email'], user_session['phone_number'],
                                         user_session['full_name'], user_session['password'])
                code_instance.delete()
                messages.success(request, 'you registred.', 'success')
            else:
                messages.error(request, 'code is wrong', 'danger')
                return redirect('accounts:verify_code')
        return redirect('home:home')

class LoginUserView(View):
    form_class = LoginUserForm

    def get(self, request):
        form = self.form_class
        return render(request, 'accounts/login.html', {'form':form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, phone_number=cd['phone_number'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'you loged in successfully', 'info')
                return redirect('home:home')
            messages.error(request, 'phone or password is wrong', 'warning')
        return render(request, 'accounts/login.html', {'form':form})

class LoginOutUserView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'your account logouted successfully', 'success')
        return redirect('home:home') 