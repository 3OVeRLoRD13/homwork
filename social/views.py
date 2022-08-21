from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post, UserFollowing
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


# follow via function based view ----------------------------------------------------------------------
@login_required(login_url='login')
def follow(request):
    if request.method == "POST":
        follower = request.user
        _user = get_object_or_404(User, username=request.POST['_user'])

        if UserFollowing.objects.filter(following_user_id=follower, user_id=_user).first():
            delete_follower = UserFollowing.objects.get(following_user_id=follower, user_id=_user)
            delete_follower.delete()
            return redirect(reverse_lazy('personal_page', args=[_user]))
        else:
            new_follower = UserFollowing.objects.create(user_id=_user, following_user_id=follower)
            new_follower.save()
            return redirect(reverse_lazy('personal_page', args=[_user]))
    else:
        return redirect(reverse_lazy('personal_page', args=[_user]))


# View user personal page via class based view ---------------------------------------------
class PersonalPageListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'social/personal_page.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_context_data(self, *args, **kwargs):
        context = super(PersonalPageListView, self).get_context_data(*args, **kwargs)
        follower_id = self.request.user.id
        user_id = get_object_or_404(User, username=self.kwargs.get('username'))

        if UserFollowing.objects.filter(following_user_id=follower_id, user_id=user_id.id).filter():
            is_follow = True
        else:
            is_follow = False

        user_followers = UserFollowing.objects.filter(user_id=user_id.id).count()
        user_following = UserFollowing.objects.filter(following_user_id=user_id).count()

        context['user_personal_page'] = user_id
        context['is_follow'] = is_follow
        context['user_followers'] = user_followers
        context['user_following'] = user_following
        return context

    def get_queryset(self):
        user_personal_page = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user_personal_page).order_by('-created_at')


# Show user posts in social page via class based view ----------------------------------------
class SocialPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'social/social.html'
    context_object_name = 'posts'
    ordering = ['-created_at']
    paginate_by = 5


# Show user followers in social page via class based view ----------------------------------------
class FollowersListView(LoginRequiredMixin, ListView):
    model = UserFollowing
    template_name = 'social/followers_list_view.html'
    ordering = ['-created_at']
    paginate_by = 5

    def get_context_data(self, *args, **kwargs):
        context = super(FollowersListView, self).get_context_data(*args, **kwargs)
        
        user_id = get_object_or_404(User, username=self.kwargs.get('username'))
        _user_followers = UserFollowing.objects.filter(user_id=user_id).order_by("-created_at")
        
        user_followers_list = []
        
        for idx, user in enumerate(_user_followers):
            user_followers_list.append(_user_followers[idx].following_user_id)
            
        paginator = Paginator(user_followers_list, self.paginate_by)        
        page = self.request.GET.get('page')

        try:
            user_followers_list = paginator.page(page)
        except PageNotAnInteger:
            user_followers_list = paginator.page(1)
        except EmptyPage:
            user_followers_list = paginator.page(paginator.num_pages)
        
        context['user_followers_list'] = user_followers_list
        return context

    def get_queryset(self):
        user_id = get_object_or_404(User, username=self.kwargs.get('username'))
        return UserFollowing.objects.filter(user_id=user_id)


# Show user followings in social page via class based view ----------------------------------------
class FollowingListView(LoginRequiredMixin, ListView):
    model = UserFollowing
    template_name = 'social/followings_list_view.html'
    ordering = ['-created_at']
    paginate_by = 5

    def get_context_data(self, *args, **kwargs):
        context = super(FollowingListView, self).get_context_data(*args, **kwargs)
        
        user_id = get_object_or_404(User, username=self.kwargs.get('username'))
        _user_followings = UserFollowing.objects.filter(following_user_id=user_id)
        user_followings_list = []
            
        for _users in _user_followings:
            user = User.objects.get(username=_users.user_id)
            user_followings_list.append(user)
            
        paginator = Paginator(user_followings_list, self.paginate_by)        
        page = self.request.GET.get('page')

        try:
            user_followings_list = paginator.page(page)
        except PageNotAnInteger:
            user_followings_list = paginator.page(1)
        except EmptyPage:
            user_followings_list = paginator.page(paginator.num_pages)
        
        context['user_followings_list'] = user_followings_list
        return context

    def get_queryset(self):
        user_id = get_object_or_404(User, username=self.kwargs.get('username'))
        return UserFollowing.objects.filter(following_user_id=user_id)

    

# Show user following posts in club page via class based view ----------------------------------------
class ClubPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'social/club.html'
    context_object_name = 'posts'
    ordering = ['-created_at']
    paginate_by = 5

    def get_context_data(self, *args, **kwargs):
        context = super(ClubPostListView, self).get_context_data(*args, **kwargs)

        user_id = get_object_or_404(User, username=self.request.user)
        _user_followings_posts_list = \
            Post.objects.filter(author__in=UserFollowing.objects.filter(following_user_id=user_id)
                                .values_list('user_id')).order_by("-created_at")

        paginator = Paginator(_user_followings_posts_list, self.paginate_by)        
        page = self.request.GET.get('page')

        try:
            _user_followings_posts_list = paginator.page(page)
        except PageNotAnInteger:
            _user_followings_posts_list = paginator.page(1)
        except EmptyPage:
            _user_followings_posts_list = paginator.page(paginator.num_pages)

        context['user_followings_posts_list'] = _user_followings_posts_list
        return context
    
    def get_queryset(self):
        user_id = get_object_or_404(User, username=self.request.user)
        _user_followings_posts_list = \
            Post.objects.filter(author__in=UserFollowing.objects.filter(following_user_id=user_id)
                                .values_list('user_id')).order_by("-created_at")
        return _user_followings_posts_list


# View detail of posts via class based view ------------------------------------------------
class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'social/post_detail_view.html'
    context_object_name = 'detail_post'


# Create posts via class based view -------------------------------------------------------
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['post_image', 'text']
    template_name = 'social/post_form.html'

    def get_success_url(self):
        messages.success(self.request, "Your Post Was Created Successfully !")
        return reverse_lazy('personal_page', args=[self.request.user.username])

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# Edit posts via class based view --------------------------------------------------------
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['text']
    template_name = 'social/edit_post_form.html'

    def get_success_url(self):
        messages.success(self.request, "Your Post Was Edited Successfully !")
        return reverse_lazy('personal_page', args=[self.request.user.username])

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


# Delete posts via class based view --------------------------------------------------------
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'social/post_confirm_delete.html'

    def get_success_url(self):
        messages.success(self.request, "Your Post Was Deleted Successfully !")
        return reverse_lazy('personal_page', args=[self.request.user.username])

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
