from django.contrib.auth.views import LogoutView, PasswordChangeView, PasswordChangeDoneView, TemplateView
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import SignUpForm
from django.urls import reverse
from django.core.mail import EmailMessage

from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from django.contrib.auth import login
from django.contrib.auth.models import User
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from .tokens import account_activation_token


class SignUpView(View):
    form_class = SignUpForm
    template_name = 'accounts/signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        email = request.POST['email']
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()

            user = form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            }
            # user.email_user(subject, message, 'zdalnenauczanieplatforma@gmail.com')
            link = reverse('activate', kwargs={
                'uidb64': message['uid'], 'token': message['token']})

            activate_url = 'http://' + current_site.domain + link

            email = EmailMessage(
                subject,
                'Hi ' + user.username + ', Please the link below to activate your account \n' + activate_url,
                'zdalnenauczanieplatforma@gmail.com',
                [email],
            )
            email.send(fail_silently=False)
            messages.success(request, 'Please Confirm your email to complete registration.')

            return redirect('confirmation_email')

        return render(request, self.template_name, {'form': form})


class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.profile.email_confirmed = True
            user.save()
            login(request, user)
            messages.success(request, 'Your account have been confirmed.')
            return redirect('home')
        else:
            messages.warning(request, ('The confirmation link was invalid, 3'
                                       'possibly because it has already been used.'))
            return redirect('home')


def signin(request):
    if request.user.is_authenticated:
        return render(request, 'home.html')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            form = AuthenticationForm(request.POST)
            return render(request, 'accounts/login.html', {'form': form})
    else:
        form = AuthenticationForm()
        return render(request, 'accounts/login.html', {'form': form})


class LogoutViewMy(LogoutView):
    template_name = 'accounts/logout.html'
    success_url = 'logout'


class PasswordChangeMy(PasswordChangeView):
    template_name = 'accounts/password_change.html'


class PasswordChangeDoneMy(PasswordChangeDoneView):
    template_name = 'accounts/password_change_done.html'


class AfterSignUpView(TemplateView):
    template_name = "accounts/confirmation_email.html"
