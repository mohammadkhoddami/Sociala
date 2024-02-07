from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.views import View
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from home.models import Post
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from .models import Relation
# Create your views here.

class RegisterView(View):
    form_class = UserRegistrationForm
    temp = 'account/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.warning(request, 'Sorry you logged in !', 'warning')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    

    def get(self, request):
        form = self.form_class()
        return render(request, self.temp, {'form' : form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd['username'], cd['email'], cd['password1'])
            messages.success(request, 'You are registered', 'success')
            return redirect('home:home')
        return render(request, self.temp, {'form': form})
        

class LoginView(View):
    form_class = UserLoginForm
    temp = 'account/login.html'


    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.warning(request, 'Sorry you logged in !', 'warning')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        form = self.form_class()
        return render(request, self.temp, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username = cd['username'], password = cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request,'You logged in successfully', 'success')
                if self.next:
                    return redirect(self.next)
                return redirect('home:home')
            messages.error(request, 'Invalid username or password', 'warning')
        return render(request, self.temp, {'form': form})


class LogoutView(LoginRequiredMixin,View):
    def get(self, request):
        logout(request)
        messages.success(request,'You logged out successfully', 'success')
        return redirect('home:home')
    

class ProfileView(LoginRequiredMixin, View):
    temp = 'account/profile.html'
    def get(self, request, user_id):
        is_following = False
        user = get_object_or_404(User, id = user_id)
        posts = user.posts.all()
        relation = Relation.objects.filter(from_user = request.user , to_user = user)
        if relation.exists():
            is_following = True
        return render(request, self.temp, {'user' : user, 'posts': posts, 'is_following' : is_following})
    

class UserPasswordResetView(auth_views.PasswordResetView):
    template_name = 'account/password_reset_form.html'
    success_url = reverse_lazy('account:password_reset_done')
    email_template_name = 'account/password_reset_email.html'


class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'account/password_reset_done.html'


class PasswordResetConfrimView(auth_views.PasswordResetConfirmView):
    template_name = 'account/password_reset_confirm.html'
    success_url = reverse_lazy('account:password_reset_complete')


class PasswordResetCompeleteView(auth_views.PasswordResetCompleteView):
    template_name = 'account/password_reset_complete.html'

class FollowView(View):
    def get(self, request, user_id):
        user = User.objects.get(id = user_id)
        relation = Relation.objects.filter(from_user = request.user , to_user = user)
        if relation.exists():
            messages.error(request, 'you already followed this user', 'warning')
        else :
            Relation(from_user = request.user , to_user = user).save()
            messages.success(request, f'{user.username} has been followed', 'success')
        return redirect('account:profile', user.id)

class UnfollowView(View):
    def get(self, request, user_id):
        user = User.objects.get(id = user_id)
        relation = Relation.objects.filter(from_user = request.user , to_user = user)
        if relation.exists():
            relation.delete()
            messages.success(request, f'You unfollowed {user.username}', 'success')
        else:
            messages.error(request, f'You are not following {user.username}', 'success')
        return redirect('account:profile', user.id)
    