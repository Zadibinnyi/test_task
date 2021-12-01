from django.contrib import admin
from django.urls import path

from film.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', FilmListView.as_view(), name='index'),
    path('login/', Login.as_view(redirect_authenticated_user=True), name='login'),
    path('register/', Register.as_view(), name='registration'),
    path('logout/', Logout.as_view(), name='logout'),
    path('addlist/', AddUserList.as_view(), name='addlist'),
    path('lists/', ListsUserView.as_view(), name='lists'),
    path('users/', UserView.as_view(), name='users'),
    path('lists/<int:pk>/', ListsView.as_view(), name="list"),
    path('lists/addfilm/<int:pk>/', AddFilmToListView.as_view(), name="add"),
    path('lists/film/<int:pk>/', FilmInListAbout.as_view(), name="about"),
    path('film/<int:pk>/', FilmAbout.as_view(), name="about_film"),
    path('lists/film/update/<int:pk>/', ListInFilmUpdateView.as_view(), name="update_filminlist"),
    path('lists/film/delete/<int:pk>/', FilmDeleteView.as_view(), name='delete_film'),
    path('lists/update/<int:pk>/', ListUserUpdateView.as_view(), name="update_list"),
    path('users/<int:pk>/', UserListsView.as_view(), name="user_lists"),
    path('users/lists/<int:pk>/', ListsUsersView.as_view(), name="lists_user"),
    path('film/comments/comment/<int:pk>/', AddCommentView.as_view(), name="add_comment"),
    path('film/comments/<int:pk>/', CommentListView.as_view(), name="comments"),
    path('film/rating/<int:pk>/', AddRatingView.as_view(), name="add_rating"),
]