from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RegisterUserForm, UserForm, ProfileForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage



# Search existing users and show them in site -----------------------------------------------
@login_required(login_url='login')
def search_users(request):
    paginate_by = 24
    
    if request.method == "POST":
        searched = request.POST['searched']
        searched_users = User.objects.filter(username__contains=searched)
        
        paginator = Paginator(searched_users, paginate_by)        
        page = request.GET.get('page')

        try:
            searched_users = paginator.page(page)
        except PageNotAnInteger:
            searched_users = paginator.page(1)
        except EmptyPage:
            searched_users = paginator.page(paginator.num_pages)
        
        return render(request, 'members/search_users.html', {'searched': searched, 'searched_users': searched_users})
    else:
        return render(request, 'members/search_users.html', {})


# Login user via function based view --------------------------------------------------------
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
        return render(request, 'members/login.html', {})


# Logout user via function based view -------------------------------------------------------
def logout_user(request):
    logout(request)
    messages.success(request, "You were Logged out Successfully !")
    return redirect('home')


# Logout user via function based view -------------------------------------------------------
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
    return render(request, 'members/register_user.html', {'form': form, })



# Change user password via class based view (Not reset password) ---------------------------
class PasswordsChangeView(auth_views.PasswordChangeView):
    template_name = 'members/change_password.html'

    def get_success_url(self):
        messages.success(self.request, "Your Password Was Changed Successfully !")
        return reverse_lazy('profile')


# View user profile via class based view
class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'members/profile.html'


# Edit user profile via class based view ---------------------------------------------------
class ProfileUpdateView(LoginRequiredMixin, TemplateView):
    user_form = UserForm
    profile_form = ProfileForm
    template_name = 'members/edit_profile.html'
    success_url = reverse_lazy('profile')

    def post(self, request):
        post_data = request.POST or None
        file_data = request.FILES or None

        user_form = UserForm(post_data, instance=request.user)
        profile_form = ProfileForm(post_data, file_data, instance=request.user.userprofile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your Profile Was Updated Successfully !")
            return redirect(reverse_lazy('profile'))

        context = self.get_context_data(user_form=user_form, profile_form=profile_form)

        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_object(self):
        return self.request.user
