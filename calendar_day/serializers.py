from rest_framework import serializers
from .models import CalendarBlock
class CalendarBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model=CalendarBlock
        fields=(
            'aula_id',
            'date'
            'start_time',
            'end_time',
            'reservation_id',
            'reservation_title',
        )
