from rest_framework import serializers
from .models import Reservation

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Reservation
        fields=(
            'id', 'aula_id', 'user_id', 'start_date', 'end_date', 'frequency', 'start_time', 'end_time','title', "reserved_for"
        )
