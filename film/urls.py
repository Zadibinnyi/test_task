from django.contrib import admin
from django.urls import path

from film.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', FilmListView.as_view(), name='index'),
    path('login/', Login.as_view(), name='login'),
    path('register/', Register.as_view(), name='registration'),
    path('logout/', Logout.as_view(), name='logout'),
    path('filter/', FilterMovieView.as_view(), name='filter'),
    path('addlist/', AddUserList.as_view(), name='addlist'),
    path('lists/', ListsUserView.as_view(), name='lists'),
    path('users/', UserView.as_view(), name='users'),
    path('lists/planned/<int:pk>/', PlannedListView.as_view(), name="planned"),
    path('lists/viewed/<int:pk>/', ViewedListView.as_view(), name="viewed"),
    path('lists/thrown/<int:pk>/', ThrownListView.as_view(), name="thrown"),
    path('lists/addfilm/<int:pk>/', AddFilmToListView.as_view(), name="add"),
    path('lists/film/<int:pk>/', FilmInListAbout.as_view(), name="about"),
    path('film/<int:pk>/', FilmAbout.as_view(), name="about_film"),
    path('lists/film/update/<int:pk>/', ListInFilmUpdateView.as_view(), name="update_filminlist"),
    path('lists/film/delete/<int:pk>/', FilmDeleteView.as_view(), name='delete_film'),
    path('lists/update/<int:pk>/', ListUserUpdateView.as_view(), name="update_list"),
    path('users/<int:pk>/', UserListsView.as_view(), name="user_lists"),
    path('film/comments/comment/<int:pk>/', AddCommentView.as_view(), name="add_comment"),
    path('film/comments/<int:pk>/', CommentListView.as_view(), name="comments"),
    path('film/rating/<int:pk>/', AddRatingView.as_view(), name="add_rating"),
]