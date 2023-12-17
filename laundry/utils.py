from datetime import datetime, timedelta
from django.utils import timezone
from .models import Reservation

def get_schedule_for_date(selected_date):
    # Pobierz rezerwacje dla wybranej daty
    start_date = datetime.combine(selected_date, datetime.min.time())
    end_date = datetime.combine(selected_date, datetime.max.time())
    reservations = Reservation.objects.filter(date__range=(start_date, end_date))

    # Utwórz słownik z harmonogramem
    schedule = {str(i).zfill(2) + ':00': '-' for i in range(24)}

    # Uzupełnij harmonogram statusami rezerwacji
    for reservation in reservations:
        start_hour = reservation.start_time.hour
        end_hour = reservation.end_time.hour

        for i in range(start_hour, end_hour):
            schedule[str(i).zfill(2) + ':00'] = 'Zarezerwowano'

    return schedule