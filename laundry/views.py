# reservations/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Reservation
from .forms import ReservationForm
from .forms import DateForm
from .utils import get_schedule_for_date
from datetime import datetime, timedelta

def reserve_laundry(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False) # przy zapisywaniu formularza, aby uzyskać dostęp do utworzonego obiektu Reservation przed zapisaniem go do bazy danych. 
            reservation.user = request.user  # Przypisz aktualnego użytkownika
            reservation.save()
            messages.success(request, 'Rezerwacja pomyślnie dokonana.')
            return redirect('laundry:schedule')
    else:
        form = ReservationForm()

    return render(request, 'reserve.html', {'form': form})

def show_schedule(request):
    selected_date = None
    schedule = None

    if request.method == 'POST':
        form = DateForm(request.POST)
        if form.is_valid():
            selected_date = form.cleaned_data['date']
            # Pobierz rezerwacje dla wybranej daty
            schedule = get_schedule_for_date(selected_date)
    else:
        form = DateForm()
        selected_date = datetime.today().date()  # Domyślnie pokazuj dzisiejsze rezerwacje
        schedule = get_schedule_for_date(selected_date)

    return render(request, 'schedule.html', {'form': form, 'schedule': schedule, 'selected_date': selected_date})

# main/views.py
def show_selected_day(request):
    date_str = request.GET.get('date', '') # np http://localhost:8000/show_selected_day/?date=December%201%2C%202023
    
    # Przekształć datę ze stringa na obiekt datetime
    date = datetime.strptime(date_str, '%B %d, %Y')
    
    day_of_week = date.weekday()
    days = ["Poniedziałek", "Wtorek", "Środa", "Czwartek", "Piątek", "Sobota", "Niedziela"]
    current_day = days[day_of_week]
    if request.method == 'POST':
        form = DateForm(request.POST)
        if form.is_valid():
            selected_date = form.cleaned_data['date']
            # Pobierz rezerwacje dla wybranej daty
            schedule = get_schedule_for_date(date)
    else:
        form = DateForm()
        selected_date = datetime.today().date()  # Domyślnie pokazuj dzisiejsze rezerwacje
        schedule = get_schedule_for_date(date)

    context = {'current_day': current_day,
               'form': form,
               'schedule': schedule,
               'selected_date': selected_date

               }
    return render(request, 'show_selected_day.html', context)

from django.shortcuts import render
from django.urls import reverse
from datetime import datetime, timedelta
from calendar import monthrange

def show_calendar(request, year=None, month=None):
    if year is None or month is None:
        today = datetime.today()
        year, month = today.year, today.month
    else:
        year, month = int(year), int(month)

    calendar_days = [i for i in range(1, monthrange(year, month)[1] + 1)]
    current_month_name = datetime(year, month, 1).strftime('%B')
    
    prev_month = month - 1 if month > 1 else 12
    prev_year = year - 1 if month == 1 else year
    next_month = month + 1 if month < 12 else 1
    next_year = year + 1 if month == 12 else year

    return render(request, 'newcalendar.html', {
        'calendar_days': calendar_days,
        'current_month_name': current_month_name,
        'current_year': year,
        'prev_year': prev_year,
        'prev_month': prev_month,
        'next_year': next_year,
        'next_month': next_month,
    })
