from django.contrib.auth.models import User, AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Avg

from film.exception import ListAlreadyCreated, FilmAlreadyAdd


class Series(models.Model):
    title = models.CharField(max_length=120)

    def __str__(self):
        return self.title


class Film(models.Model):
    title = models.CharField(max_length=120)
    series = models.ForeignKey(Series, on_delete=models.CASCADE, related_name='filmseries', null=True, blank=True)
    rank = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.title


class Genres(models.Model):
    title = models.CharField(max_length=120)

    def __str__(self):
        return self.title


class GenresFilm(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='filmganre')
    ganre = models.ForeignKey(Genres, on_delete=models.CASCADE, related_name='ganrefilm')

    def __str__(self):
        return f"{self.film.title} is {self.ganre.title}"


class Lists(models.Model):
    title = models.CharField(max_length=120)

    def __str__(self):
        return self.title


class ListsUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userlist')
    lists = models.ForeignKey(Lists, on_delete=models.CASCADE, related_name='listsuser')
    access = models.BooleanField(default=True)

    def __str__(self):
        return self.lists.title

    def save(self, *args, **kwargs):
        if ListsUser.objects.filter(lists_id=self.lists.id):
            raise ListAlreadyCreated()
        else:
            super(ListsUser, self).save(*args, **kwargs)


class FilmListsUser(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='filmlistuser')
    listsuser = models.ForeignKey(ListsUser, on_delete=models.CASCADE, related_name='listsuserfilm')

    def __str__(self):
        return f"{self.listsuser.user}"

    def save(self, *args, **kwargs):
        if FilmListsUser.objects.filter(listsuser_id=self.listsuser.id, film_id=self.film.id):
            raise FilmAlreadyAdd()
        else:
            super(FilmListsUser, self).save(*args, **kwargs)


class Comment(models.Model):
    text = models.TextField()
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='filmcomment')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='usercomment')

    def __str__(self):
        return self.text


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='rating')
    rating = models.IntegerField(
        default=1, validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    def __str__(self):
        return f"{self.film}, {self.rating}"

    def save(self, *args, **kwargs):
        super(Rating, self).save(*args, **kwargs)
        self.film.rank = Rating.objects.filter(film_id=self.film.id).aggregate(Avg('rating')).__getitem__('rating__avg')
        self.film.save()

