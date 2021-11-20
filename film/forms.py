from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm


from .models import *


class Registration(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', ]


class FilmCreateForm(ModelForm):

    class Meta:
        model = Film
        fields = ['title', ]


class AddListToUserForm(ModelForm):

    class Meta:
        model = ListsUser
        fields = ['lists', 'access', ]


class AddFilmToListForm(ModelForm):

    class Meta:
        model = FilmListsUser
        fields = ['listsuser', ]


class CommentForm(ModelForm):

    class Meta:
        model = Comment
        fields = ['text', ]


class RatingForm(ModelForm):

    class Meta:
        model = Rating
        fields = ['rating', ]