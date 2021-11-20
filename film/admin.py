from django.contrib import admin
from .models import *

admin.site.register(Film)
admin.site.register(Genres)
admin.site.register(Lists)
admin.site.register(GenresFilm)
admin.site.register(ListsUser)
admin.site.register(FilmListsUser)
admin.site.register(Comment)
admin.site.register(Series)
admin.site.register(Rating)
