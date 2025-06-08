from django.db import models
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields


class GenreModel(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(max_length=100, verbose_name=_('Name'))
    )

    class Meta:
        db_table = 'genre'
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')

    def __str__(self):
        return self.name


class DirectorModel(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(max_length=100, verbose_name=_('Name')),
        surname = models.CharField(max_length=100, verbose_name=_('Surname'))
    )
    image = models.ImageField(upload_to='directors/', null=True, blank=True)

    class Meta:
        db_table = 'directors'
        verbose_name = _('Director')
        verbose_name_plural = _('Directors')

    def __str__(self):
        return self.name


class ActorModel(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(max_length=100, verbose_name=_('Name')),
        surname = models.CharField(max_length=100, verbose_name=_('Surname'))
    )
    image = models.ImageField(upload_to='actors/', null=True, blank=True)

    class Meta:
        db_table = 'actors'
        verbose_name = _('Actor')
        verbose_name_plural = _('Actors')

    def __str__(self):
        return self.name


class MovieModel(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=128, verbose_name=_('Name')),
        description = models.TextField(verbose_name=_('Description')),
    )
    certificate = models.PositiveSmallIntegerField(verbose_name=_('Certificate'))
    runtime = models.TimeField(verbose_name=_('Runtime'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'))
    released = models.DateTimeField(verbose_name=_('Released'))
    genres = models.ManyToManyField(GenreModel, verbose_name=_('Genres'))
    actors = models.ManyToManyField(ActorModel, verbose_name=_('Actors'))
    directors = models.ManyToManyField(DirectorModel, related_name='films', verbose_name=_('Directors'))

    image = models.ImageField(upload_to='movie_images', verbose_name=_('Movie image'))
    trailer = models.FileField(upload_to='movie_trailers', verbose_name=_('Movie trailer'))

    class Meta:
        db_table = 'movies'
        verbose_name = _('Movie')
        verbose_name_plural = _('Movies')

    def __str__(self):
        return self.name


class RatingModel(models.Model):
    platform = models.CharField(max_length=128, verbose_name=_('Platform'))
    rating = models.IntegerField(verbose_name=_('Rating'))
    movie = models.ForeignKey(MovieModel, on_delete=models.CASCADE, related_name='ratings', verbose_name=_('Movie'))

    class Meta:
        db_table = 'ratings'
        verbose_name = _('Rating')
        verbose_name_plural = _('Ratings')

    def __str__(self):
        return f"{self.platform} - {self.rating}"


class CinemaModel(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=128, verbose_name=_('Name')),
        description=models.TextField(verbose_name=_('Description')),
        address=models.TextField(verbose_name=_('Address')),
    )
    seats_row_count = models.PositiveIntegerField(verbose_name=_('Seats row count'))
    seats_column_count = models.PositiveIntegerField(verbose_name=_('Seats column count'))

    class Meta:
        db_table = 'cinemas'
        verbose_name = _('Cinema')
        verbose_name_plural = _('Cinemas')

    def __str__(self):
        return self.name


class SessionModel(models.Model):
    time = models.TimeField(verbose_name=_('Time'))
    options: list[str] = models.JSONField(default=list[str], verbose_name=_('Options'))
    movie = models.ForeignKey(MovieModel, on_delete=models.CASCADE, related_name='sessions', verbose_name=_('Movie'))
    cinema = models.ForeignKey(CinemaModel, on_delete=models.CASCADE, verbose_name=_('Cinema'))

    class Meta:
        db_table = 'sessions'
        verbose_name = _('Session')
        verbose_name_plural = _('Sessions')

    def __str__(self):
        return f"{self.time}: {', '.join(self.options)}"


class PriceType(models.TextChoices):
    ADULT = "A", _("Adult")
    CHILDREN = "K", _("Children")
    STUDENT = "S", _("Student")
    VIP = "V", _("VIP")


class PriceModel(models.Model):
    type = models.CharField(max_length=128, verbose_name=_('Price'), choices=PriceType.choices)
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name=_('Price'))
    session = models.ForeignKey(SessionModel, on_delete=models.CASCADE, related_name='price', verbose_name=_('Session'))

    class Meta:
        db_table = 'prices'
        verbose_name = _('Price')
        verbose_name_plural = _('Prices')

    def __str__(self):
        return f"{self.type}: {self.price}"


class TicketModel(models.Model):
    session = models.ForeignKey(SessionModel, on_delete=models.CASCADE, related_name='tickets', verbose_name=_('Session'))
    price = models.ForeignKey(PriceModel, on_delete=models.CASCADE, related_name='tickets', verbose_name=_('Price'))
    seat_row = models.PositiveIntegerField(verbose_name=_('Seat row'))
    seat_column = models.PositiveIntegerField(verbose_name=_('Seat column'))

    class Meta:
        db_table = 'tickets'
        verbose_name = _('Ticket')
        verbose_name_plural = _('Tickets')

    def __str__(self):
        return f"{self.session}: {self.price}"
