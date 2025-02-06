from django.db import models
from django.core.validators import MaxValueValidator
from aulas.models import Aula
from reservations.models import Reservation
from datetime import date
from django.utils import timezone
# Create your models here.

class CalendarBlock(models.Model):
    aula_id = models.ForeignKey(Aula, related_name='calendar_block', on_delete=models.CASCADE)
    date= models.DateField(null=False, blank=False, default=date.today())
    start_time= models.TimeField(null=False, blank=False, default=timezone.now().time())
    end_time= models.TimeField(null=False, blank=False, default=timezone.now().time())
    reservation_id = models.ForeignKey(Reservation, related_name="calendar_block", related_query_name='calendar_block', on_delete=models.CASCADE)
    reservation_title = models.TextField(blank=False, null=False)
    def __str__(self):
        return f"Aula {self.aula_id.name} {self.date} {self.start_time.strftime('%H:%M:%S')} - {self.end_time.strftime('%H:%M:%S')}"
