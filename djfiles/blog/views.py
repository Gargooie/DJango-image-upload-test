import csv

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import ListView

from .models import BlogPost, Profile, PostPhotosModel
from .forms import RegisterForm, ProfilePageForm, CreatePostForm, PhotosLoadForm, UploadPostsFile


class MainPageView(ListView):
    model = BlogPost
    template_name = 'index.html'

    def get_context_data(self, *args, **kwargs):
        blog_posts_list = BlogPost.objects.all()
        author = Profile.objects.select_related('user')

        context = super().get_context_data(*args, **kwargs)
        context['blog_list'] = blog_posts_list
        context['author'] = author
        return context


class UserLoginView(LoginView):
    template_name = 'login.html'


class UserLogoutView(LogoutView):
    template_name = 'logout.html'


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            avatar = form.cleaned_data['avatar']
            Profile.objects.create(
                user=user,
                avatar=avatar
            )
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/profile')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def account_view(request):
    user = User.objects.get(username=request.user.username)
    return render(request, 'profile_page.html', {"user": user})


def profile_page_view(request):
    if request.method == 'POST':
        form = ProfilePageForm(request.POST, request.FILES)
        if form.is_valid():
            user = request.user
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            about_me = form.cleaned_data.get('about_me')
            Profile.objects.filter(user_id=user).update(about_me=about_me)
            User.objects.filter(id=request.user.id).update(first_name=first_name, last_name=last_name, email=email)

            if not form.cleaned_data.get('avatar') is None:
                if request.FILES.get('avatar'):
                    avatar = request.FILES['avatar']
                else:
                    avatar = 0
                profile_obj = Profile.objects.filter(user_id=user).get()
                profile_obj.avatar = avatar
                profile_obj.save()

        return HttpResponseRedirect('/profile')

    else:
        user = request.user
        first_name = request.user.first_name
        last_name = request.user.last_name
        email = request.user.email
        avatar = request.user.profile.avatar
        about_me = request.user.profile.about_me
        form = ProfilePageForm(initial={'user': user, 'avatar': avatar, 'about_me': about_me, 'first_name': first_name,
                                        'last_name': last_name, 'email': email})

    return render(request, 'profile_page.html', {'form': form})


def create_post_view(request):
    if request.method == 'POST':
        if 'hand_post' in request.POST:
            form_text = CreatePostForm(request.POST)
            if form_text.is_valid():
                content = form_text.cleaned_data['content']
                BlogPost.objects.create(content=content, author=request.user)
                profile_obj = Profile.objects.filter(user_id=request.user).get()
                profile_obj.posts_count += 1
                profile_obj.save()

                form_photo = PhotosLoadForm(request.POST, request.FILES)
                if form_photo.is_valid():
                    photos = request.FILES.getlist('photos')
                    for photo in photos:
                        blog_post = BlogPost.objects.filter(author=request.user).get()
                        instance = PostPhotosModel(photos=photo, blog_post=blog_post)
                        instance.save()
                        profile_obj = Profile.objects.filter(user_id=request.user).get()
                        profile_obj.posts_count += 1
                        profile_obj.save()
                    return HttpResponseRedirect('/')
        elif 'file_post' in request.POST:
            form_file = UploadPostsFile(request.POST, request.FILES)
            if form_file.is_valid():
                posts = form_file.cleaned_data['posts'].read().decode('utf-8').split('\n')

                csv_reader = csv.reader(posts, delimiter='/')
                for row in csv_reader:
                    if row:
                        blog_post = BlogPost.objects.create(content=row[0], author=request.user)
                        blog_post.created_at = row[1]
                        blog_post.save()
                return HttpResponseRedirect('/')

    else:
        form_text = CreatePostForm()
        form_photo = PhotosLoadForm()
        form_file = UploadPostsFile()
        return render(request, 'create_post.html', context={'form_text': form_text, 'form_photo': form_photo,
                                                            'form_file': form_file})


def detail_post_view(request, post_id):
    blog_post = BlogPost.objects.get(id=post_id)
    photos = PostPhotosModel.objects.filter(blog_post=blog_post)
    return render(request, 'post_detail.html', context={'blog_post': blog_post, 'photos': photos})
