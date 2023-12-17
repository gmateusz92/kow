# main/models.py
from django.db import models
from django.contrib.auth.models import User

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    

    def __str__(self):
        # Formatuj godziny za pomocą strftime, aby uzyskać tylko godziny (bez minut)
        start_time_str = self.start_time.strftime('%H:%M')
        end_time_str = self.end_time.strftime('%H:%M')

        return f"{self.user.username} - {self.date} {start_time_str}-{end_time_str}"