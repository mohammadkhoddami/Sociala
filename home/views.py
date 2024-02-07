from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import PostUpdateForm
from django.utils.text import slugify

# Create your views here.

class HomeView(View):
    temp = 'home/index.html'
    def get(self, request):
        posts = Post.objects.all()
        return render(request, self.temp, {'posts': posts})
    

class PostView(View):
    temp = 'home/post.html'
    def get(self, request, post_id, post_slug):
        post = get_object_or_404(Post, id = post_id, slug = post_slug)
        return render(request, self.temp, {'post': post})
    
class DeleteView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = get_object_or_404(Post,id = post_id)
        if post.user.id == request.user.id:
            post.delete()
            messages.success(request, 'Your post has been deleted', 'success')
        else:
            messages.error(request, 'Your are not the author !', 'danger')
        return redirect('home:home')
    

class UpdateView(LoginRequiredMixin, View):
    form_class = PostUpdateForm
    temp = 'home/update.html'

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post,pk = kwargs['post_id'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        post = self.post_instance
        if not post.user.id == request.user.id:
            messages.error(request, 'You are not the Author', 'warning')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form_class(instance= post)
        return render(request, self.temp, {'form': form})

    def post(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form_class(request.POST, instance= post)
        if form.is_valid():
            new_post = form.save(commit= False)
            new_post.slug = slugify(form.cleaned_data['body'][:30])
            new_post.save()
            messages.success(request, 'Your Post has been upgraded', 'success')
            return redirect('home:post', post.id, new_post.slug)
        

class CreateView(LoginRequiredMixin, View):
    form_class = PostUpdateForm
    temp = 'home/create.html'
    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, self.temp, {'form': form})

    def post(self, request,*args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_post = form.save(commit= False)
            new_post.slug = slugify(form.cleaned_data['body'][:30])
            new_post.user = request.user
            new_post.save()
            messages.success(request, 'Your Post is created', 'success')
            return redirect('home:post', new_post.id, new_post.slug)


