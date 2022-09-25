from django.db import models

from movies.models import Movie


class Hall(models.Model):
    # TODO we probably dont want this to be null
    name = models.CharField(max_length=50, null=True)

    def __str__(self):
        return f'{self.name}'


class Showtime(models.Model):
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    time = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        """
        Overrides default save method. 
        Creates new empty seats for the new show.
        """
        # NOTE we create this seats to be small first so its more
        # managable
        super().save(*args, **kwargs)
        ROW = 5
        SEAT_NUM = 10
        for i in range(1, ROW + 1):
            for j in range(1, SEAT_NUM + 1):
                s = Seat(
                    row_number=i,
                    seat_number=j,
                    status='O',
                    vip=i % 5 == 3,  # For now VIP seats are row 3
                    hall=self.hall,
                    showtime=self,
                )
                s.save()

    def __str__(self):
        return f'{self.movie} - {self.hall} ({self.time})'


class Seat(models.Model):
    SEAT_STATUS = [
        ('X', 'Seat Taken'),
        ('O', 'Seat Available'),
        ('*', 'Seat Being Booked')
    ]

    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, null=False)
    row_number = models.PositiveSmallIntegerField()
    seat_number = models.PositiveSmallIntegerField()
    vip = models.BooleanField(default=False)
    status = models.CharField(max_length=1, choices=SEAT_STATUS)
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'Seat ({self.row_number}, {self.seat_number})'

    # def to_string(self):
    #     return f'ROW: {self.row_number} No.{self.seat_number}'
