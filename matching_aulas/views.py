from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from aulas.models import Aula
from calendar_day.models import CalendarBlock
from aulas.serializers import AulaSerializer
from datetime import datetime, timedelta, time
from dateutil.relativedelta import relativedelta
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.exceptions import ValidationError
from django.utils import timezone

class MatchingAulasView(generics.ListAPIView):
    permission_classes=[permissions.IsAuthenticated]
    queryset = Aula.objects.all()
    serializer_class = AulaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['max_capacity']
    
    def get_queryset(self):
        queryset = super().get_queryset()

        if not self.request.query_params:
            raise ValidationError("All parameters missing")
        
        # Get the parameters from the request
        capacity = int(self.request.query_params.get('capacity'))
        has_negatoscope = self.request.query_params.get('has_negatoscope') == 'true'
        has_screen = self.request.query_params.get('has_screen') == 'true'
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        frequency = self.request.query_params.get('frequency')
        start_time = self.request.query_params.get('start_time')
        end_time = self.request.query_params.get('end_time')
        
        # List of parameters
        params = ['capacity', 'has_negatoscope', 'has_screen', 'start_date', 'end_date', 'frequency', 'start_time', 'end_time']

        # Check if the required parameters are present
        missing_params = [param for param in params if self.request.query_params.get(param) is None]
        if missing_params:
            raise ValidationError(f"Required parameters are missing: {', '.join(missing_params)}")
    
       
        
        # Convert the start_date and end_date strings to date objects
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

        # Make the start_date and end_date timezone-aware
        start_date = timezone.make_aware(datetime.combine(start_date, time()))
        end_date = timezone.make_aware(datetime.combine(end_date, time()))

        # Map frequencies to their corresponding timedelta arguments
        frequency_map = {
            'daily': timedelta(days=1),
            'weekly': timedelta(weeks=1),
            'monthly': relativedelta(months=1),
            'none': timedelta(days=1) # No increment
        }

        # Exclude Aula objects that have conflicting CalendarBlock objects
        queryset = queryset.exclude(
            Q(max_capacity__lt=capacity)
        )

        
        # Add conditions to the queryset only if the request arguments are 'true'
        if has_negatoscope:
            queryset = queryset.filter(has_negatoscope=False)
        if has_screen:
            queryset = queryset.exclude(has_screen=False)

        # Generate potential dates for the reservation
        current_date = start_date

        # Prepare the dates and times for the query
        dates = []
        while current_date <= end_date:
            dates.append((current_date, start_time, end_time))
            current_date += frequency_map.get(frequency, timedelta(1))

        q_objects = Q()

        for date, start_time, end_time in dates:
            q_objects |= Q(date=date, start_time=start_time, end_time=end_time)

        conflicting_blocks = CalendarBlock.objects.filter(q_objects)
        

        # Extract aula_id values from conflicting_blocks and convert to a set to remove duplicates
        aula_ids_to_exclude = set(conflicting_blocks.values_list('aula_id', flat=True))

        # Exclude the aula objects that have calendar_blocks in the conflicting_blocks queryset
        queryset = queryset.exclude(id__in=aula_ids_to_exclude)


        # Order the remaining Aula objects by max_capacity
        queryset = queryset.order_by('max_capacity')

        # Limit the queryset to the first three objects
        queryset = queryset[:3] 

        return queryset

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if not queryset.exists():
            return Response([], status=200)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=200)
