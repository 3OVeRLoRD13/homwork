from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import RegisterUserForm, UserForm, ProfileForm
from django.views.generic import TemplateView
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post


def search_users(request):
    if request.method == "POST":
        searched = request.POST['searched']
        searched_users = User.objects.filter(username__contains=searched)
        return render(request, 'search_users.html', {'searched':searched, 'searched_users':searched_users})
    else:
        return render(request, 'search_users.html', {})


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login Successful !")
            return redirect('profile')
        else:
            messages.success(request, "There was an Error Logging In, Try Again !")
            return redirect('login')
    else:
        return render(request, 'login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, "You were Logged out Successfully !")
    return redirect('home')


def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Registration Successful !")
            return redirect('profile')
    else:
        form = RegisterUserForm()
    return render(request, 'register_user.html', {'form': form, })


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'


class ProfileUpdateView(LoginRequiredMixin, TemplateView):
    user_form = UserForm
    profile_form = ProfileForm
    template_name = 'edit_profile.html'
    success_url = reverse_lazy('profile')

    def post(self, request):
        post_data = request.POST or None
        file_data = request.FILES or None

        user_form = UserForm(post_data, instance=request.user)
        profile_form = ProfileForm(post_data, file_data, instance=request.user.userprofile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile was successfully updated !")
            return redirect(reverse_lazy('profile'))

        context = self.get_context_data(user_form=user_form, profile_form=profile_form)

        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_object(self):
        return self.request.user


class PersonalPageListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'personal_page.html'
    context_object_name = 'posts'
    ordering = ['-created_at']


class PostListView(ListView):
    model = Post
    template_name = 'social.html'
    context_object_name = 'posts'
    ordering = ['-created_at']


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail_view.html'
    context_object_name = 'detail_post'


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['text']
    template_name = 'post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['text']
    template_name = 'post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

# test comment
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'post_confirm_delete.html'
    success_url = reverse_lazy('personal_page')

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
