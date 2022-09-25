from django.db import models


class Movie(models.Model):
    CERTIFICATION_TYPES = [
        ('U'    , 'U'), 
        ('PG'   , 'PG'), 
        ('12'   , '12'), 
        ('12A'  , '12A'), 
        ('15'   , '15'), 
        ('18'   , '18'), 
        ('R18'  , 'R18'),
    ]

    title           = models.CharField(max_length=100)
    director        = models.TextField(max_length=500)
    lead_actor      = models.TextField(max_length=100)
    certificate     = models.CharField(max_length=3, choices=CERTIFICATION_TYPES)
    duration        = models.PositiveSmallIntegerField()
    rating          = models.DecimalField(max_digits=3, decimal_places=1)
    premier_date    = models.DateField(null=True)
    blurb           = models.TextField(max_length=1000, blank=True)

    def __str__(self):
        return f'{self.title} ({self.premier_date.year})'
