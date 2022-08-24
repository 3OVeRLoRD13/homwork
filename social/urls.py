from django.urls import path
from .views import *


urlpatterns = [
    # Follow view ---------------------------------------------------------------------------
    path('follow/', follow, name='follow'), # follow path
    # social and club page view -------------------------------------------------------------
    path('', SocialPostListView.as_view(), name='social'),  # Social path
    path('club/', ClubPostListView.as_view(), name='club'),  # Clube path
    # Personal page view --------------------------------------------------------------------
    path('personal_page/<str:username>/', PersonalPageListView.as_view(), name='personal_page'),  # Users personal page
    # Follow view ---------------------------------------------------------------------------
    path('personal_page/<str:username>/followers/', FollowersListView.as_view(), name='followers'),  # followers path
    path('personal_page/<str:username>/followings/', FollowingListView.as_view(), name='followings'),  # followings path
    # Post views ----------------------------------------------------------------------------
    path('like/<int:pk>/post/', AddLikes.as_view(), name='like_post'),  # Like post
    path('dislike/<int:pk>/post/', AddDisLikes.as_view(), name='dislike_post'),  # Dislike post
    path('post/new/', PostCreateView.as_view(), name='create_post'),  # Create post
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail_view'),  # Detail post
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='post_edit_view'),  # Edit post
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete_view'),  # Delete post
    # Comment views -------------------------------------------------------------------------
    path('post/<int:post_pk>/comment/<int:pk>/reply/', CommentReplyView.as_view(), name='reply_comment'),  # Like comment
    path('post/<int:post_pk>/comment/<int:pk>/like/', AddCommentLikes.as_view(), name='like_comment'),  # Like comment
    path('post/<int:post_pk>/comment/<int:pk>/dislike/', AddCommentDisLikes.as_view(), name='dislike_comment'),  # Dislike comment
    path('post/<int:post_pk>/comment/delete/<int:pk>/', CommentDeleteView.as_view(), name='comment_delete_view'),  # Delete comment
    # ---------------------------------------------------------------------------------------
]