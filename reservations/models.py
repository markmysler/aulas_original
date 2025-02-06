from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta, date
from django.db import transaction
from aulas.models import Aula
from dateutil.relativedelta import relativedelta
from django.utils import timezone
# Create your models here.

class Reservation(models.Model):
    aula_id = models.ForeignKey(Aula, related_name='reservations', on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, related_name='reservations', on_delete=models.CASCADE)
    start_date = models.DateField(null=False, blank=False, default=date.today())
    end_date = models.DateField(null=False, blank=False, default=date.today())
    frequency = models.CharField(
        max_length=255,
        blank=False,
        null=False
    )
    start_time = models.TimeField(null=False, blank=False, default=timezone.now().time())
    end_time = models.TimeField(null=False, blank=False, default=timezone.now().time())
    title = models.TextField(max_length=255, null=False, blank=False)
    reserved_for = models.TextField(max_length=255, null=False, blank=False, default="")
    
    def __str__(self):
        return f"{self.title} de {self.user_id}"

    def save(self, *args, **kwargs):
        from calendar_day.models import CalendarBlock
        # Call the original save method
        super().save(*args, **kwargs)

        # Calculate the start and end dates
        start_date = self.start_date
        end_date = self.end_date

        # Create a list to hold all the dates
        dates = []

        frequency_map = {
            'daily': timedelta(days=1),
            'weekly': timedelta(weeks=1),
            'monthly': relativedelta(months=1),
            'none': timedelta(days=1)
        }
        
        # While the start date is less than or equal to the end date
        current_date = start_date
        while current_date <= end_date:
            # Add the current date to the list
            dates.append(current_date)

            # Increment the start date by one week
            current_date += frequency_map.get(self.frequency, timedelta(1))

        # Start a database transaction
        with transaction.atomic():
            # For each date in the dates list
            for date in dates:
                if date.weekday() != 6:
                    # Create a new CalendarBlock object
                    CalendarBlock.objects.create(
                        aula_id=self.aula_id,
                        date=date,
                        start_time=self.start_time,
                        end_time=self.end_time,
                        reservation_id=self,
                        reservation_title=self.title
                    )
