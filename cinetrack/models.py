from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError


class Title(models.Model):

    TYPE_CHOICES = [
        ('movie', 'Movie'),
        ('show', 'Show'),
    ]

    # INDEXES ADDED
    name = models.CharField( max_length=255, db_index=True)  # index for title search

    release_year = models.IntegerField(db_index=True)  # index for filter by year

    type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        db_index=True 
    )  # index for filter by movie/show

    rating = models.IntegerField(
        validators=[ MinValueValidator(0), MaxValueValidator(10)],
        db_index=True  
    ) # index for filter by min_rating


    def clean(self):
        if self.release_year < 1000 or self.release_year > 9999:
            raise ValidationError("Release year must be exactly 4 digits.")

    def __str__(self):
        return f"{self.name} ({self.release_year})"

    class Meta:
        indexes = [
            models.Index(fields=['type', 'release_year']),
        ]