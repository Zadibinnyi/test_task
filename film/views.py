from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib import messages

from film.forms import Registration, AddListToUserForm, AddFilmToListForm, CommentForm, RatingForm
from film.models import *


class GenreFilter:

    def get_ganres(self):
        return Genres.objects.all()


class Login(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        return '/'.format(self.request.user.id)


class Register(CreateView):
    form_class = Registration
    template_name = 'registration.html'
    success_url = '/'


class Logout(LoginRequiredMixin, LogoutView):
    next_page = '/'
    login_url = 'login/'


class FilmListView(GenreFilter, ListView):
    model = Film
    queryset = Film.objects.all()
    template_name = 'index.html'
    paginate_by = 2

    def get_queryset(self):
        context = self.request.GET.get('ganre')
        if context is None:
            queryset = Film.objects.all()
        else:
            queryset = Film.objects.filter(filmganre__ganre__title=context)
        return queryset


class AddUserList(LoginRequiredMixin, CreateView):
    login_url = 'login/'
    form_class = AddListToUserForm
    success_url = '/'
    template_name = 'addlisttouser.html'

    def get_success_url(self):
        return "/".format(self.request.user.id)

    def form_valid(self, form):
        try:
            userlist = form.save(commit=False)
            userlist.user = self.request.user
            userlist.save()
            return HttpResponseRedirect(self.get_success_url())
        except ListAlreadyCreated:
            return messages.error(self.request, "List already created!")
        finally:
            return redirect(f"/addlist/")


class ListsUserView(ListView):
    model = ListsUser
    template_name = 'lists.html'


class ListUserUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'login/'
    template_name = 'update_list.html'
    model = ListsUser
    fields = ['access', ]
    success_url = '/'


class ListsView(ListView):
    pk_url_kwarg = "pk"
    model = FilmListsUser
    template_name = "list.html"

    def get_queryset(self):
        queryset = FilmListsUser.objects.filter(listsuser=self.kwargs["pk"])
        return queryset


class ListsUsersView(ListView):
    pk_url_kwarg = "pk"
    model = FilmListsUser
    template_name = "filmuserslist.html"

    def get_queryset(self):
        queryset = FilmListsUser.objects.filter(listsuser=self.kwargs["pk"])
        return queryset


class AddFilmToListView(LoginRequiredMixin, CreateView):
    pk_url_kwarg = "pk"
    login_url = "/login/"
    form_class = AddFilmToListForm
    template_name = "add_film.html"

    def form_valid(self, form):
        try:
            lists = form.save(commit=False)
            lists.film = Film.objects.get(pk=self.kwargs["pk"])
            lists.save()
            return messages.error(self.request, "Added!")
        except FilmAlreadyAdd:
            return messages.error(self.request, "Film alredy added to this list!")
        finally:
            return redirect(f"/lists/addfilm/{self.kwargs['pk']}")

    def get_form(self):
        form = super(AddFilmToListView, self).get_form(AddFilmToListForm)
        form.fields['listsuser'].queryset = ListsUser.objects.filter(user=self.request.user)
        return form


class CommentListView(ListView):
    pk_url_kwarg = "pk"
    model = Comment
    template_name = "film_comments.html"

    def get_queryset(self):
        return Comment.objects.filter(film_id=self.kwargs["pk"])


class AddRatingView(LoginRequiredMixin, CreateView):
    pk_url_kwarg = "pk"
    login_url = "/login/"
    form_class = RatingForm

    def post(self, request, **kwargs):
        try:
            form = RatingForm(request.POST)
            if form.is_valid():
                Rating.objects.update_or_create(
                    user=self.request.user,
                    film=Film.objects.get(pk=self.kwargs["pk"]),
                    defaults={'rating': int(request.POST.get("rating"))}
                )
                return HttpResponseRedirect(self.get_success_url())
        except RatingValueError:
            return messages.error(self.request, "Rating must be grate 0 and less or equal 5")
        finally:
            return redirect(self.get_success_url())

    def get_success_url(self):
        return f"/film/{self.kwargs['pk']}"


class FilmAbout(DetailView):
    pk_url_kwarg = "pk"
    model = Film
    template_name = "film.html"
    extra_context = {"comment": CommentForm, "film": FilmListView.queryset.values(),
                     "rating": RatingForm}


class FilmInListAbout(DetailView):
    pk_url_kwarg = "pk"
    model = FilmListsUser
    template_name = "filmlist.html"


class FilmDeleteView(LoginRequiredMixin, DeleteView):
    pk_url_kwarg = "pk"
    model = FilmListsUser
    success_url = '/lists/'


class ListInFilmUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'login/'
    template_name = 'update_filminlist.html'
    model = FilmListsUser
    fields = ['listsuser']
    success_url = '/'

    def form_valid(self, form):
        try:
            lists = form.save(commit=False)
            lists.save()
            return messages.error(self.request, "Changed!")
        except FilmAlreadyAdd:
            return messages.error(self.request, "Film alredy in this list!")
        finally:
            return redirect(f"/lists/film/update/{self.kwargs['pk']}")

    def get_form(self):
        form = super(ListInFilmUpdateView, self).get_form(AddFilmToListForm)
        form.fields['listsuser'].queryset = ListsUser.objects.filter(user=self.request.user)
        return form


class UserView(ListView):
    model = User
    template_name = 'users.html'


class UserListsView(ListView):
    pk_url_kwarg = "pk"
    model = ListsUser
    template_name = "userlists.html"

    def get_queryset(self):
        return ListsUser.objects.filter(user_id=self.kwargs["pk"])


class AddCommentView(LoginRequiredMixin, CreateView):
    pk_url_kwarg = "pk"
    login_url = "/login/"
    form_class = CommentForm

    def form_valid(self, form):
            comment = form.save(commit=False)
            comment.user = self.request.user
            comment.film = Film.objects.get(pk=self.kwargs["pk"])
            comment.save()
            return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return f"/film/comments/{self.kwargs['pk']}"


