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
from django.shortcuts import render
from datetime import datetime, timedelta
from .models import Reservation
from .forms import DateForm
from .utils import get_schedule_for_date

def show_schedule_by_day(request, day_of_week):
    # Mapowanie nazw dni tygodnia na ich numer (poniedziałek: 0, wtorek: 1, ..., niedziela: 6)
    days_mapping = {
        'poniedziałek': 0,
        'wtorek': 1,
        'środa': 2,
        'czwartek': 3,
        'piątek': 4,
        'sobota': 5,
        'niedziela': 6,
    }

    # Sprawdź, czy podany dzień tygodnia istnieje w słowniku
    if day_of_week.lower() not in days_mapping:
        return render(request, 'invalid_day.html')

    # Przekształć nazwę dnia tygodnia na numer
    day_number = days_mapping[day_of_week.lower()]

    # Oblicz datę dla danego dnia tygodnia
    today = datetime.today()
    selected_date = today - timedelta(days=today.weekday()) + timedelta(days=day_number)
    schedule = get_schedule_for_date(selected_date)

    return render(request, 'schedule_by_day.html', {'selected_date': selected_date, 'schedule': schedule})


from django.shortcuts import render

def my_view(request):
    # ... inne elementy kontekstu ...
    days_of_week = ['poniedziałek', 'wtorek', 'środa', 'czwartek', 'piątek', 'sobota', 'niedziela']
    return render(request, 'schedule_with_datepicker.html', {'days_of_week': days_of_week})