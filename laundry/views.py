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

def show_today(request):
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

from .models import Reservation  # Importuj model rezerwacji

def get_reservations_for_date(selected_date):
    reservations = Reservation.objects.filter(date=selected_date)
    return reservations

from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

@method_decorator(csrf_protect, name='dispatch')
class ShowSelectedDayView(View):
    template_name = 'show_selected_dayy.html'

    def get(self, request, *args, **kwargs):
        date_str = request.GET.get('date', '')
        
        # Przekształć datę ze stringa na obiekt datetime
        date = datetime.today().date()  # Domyślnie dzisiejsza data
        if date_str:
            try:
                date = datetime.strptime(date_str, '%B %d, %Y')
            except ValueError:
                # Dodaj obsługę błędu, na przykład przypisz dzisiejszą datę
                pass
        
        day_of_week = date.weekday()
        days = ["Poniedziałek", "Wtorek", "Środa", "Czwartek", "Piątek", "Sobota", "Niedziela"]
        current_day = days[day_of_week]
        
        form = DateForm()
        schedule = get_schedule_for_date(date)
        reservation_form = ReservationForm()
        reservations = get_reservations_for_date(date)
        
        return render(request, self.template_name, {
            'form': form,
            'current_day': current_day,
            'schedule': schedule,
            'selected_date': date,
            'reservation_form': reservation_form,
            'reservations': reservations
        })

    def post(self, request, *args, **kwargs):
        form = DateForm(request.POST)
        if form.is_valid():
            selected_date = form.cleaned_data['date']
            schedule = get_schedule_for_date(selected_date)
            
            # Popraw: Przekazuj dane z żądania do formularza rezerwacji
            reservation_form = ReservationForm(request.POST)
            
            if reservation_form.is_valid():
                # Popraw: Zapisz rezerwację tylko jeśli formularz rezerwacji jest prawidłowy
                reservation = reservation_form.save(commit=False)
                reservation.user = request.user
                reservation.date = selected_date
                reservation.save()
                return redirect('laundry:show_selected_dayy')
                
            reservations = get_reservations_for_date(selected_date)
            return render(request, self.template_name, {
                'form': form,
                'current_day': selected_date.strftime('%A'),
                'schedule': schedule,
                'selected_date': selected_date,
                'reservation_form': reservation_form,
                'reservations': reservations
            })
        return render(request, self.template_name, {'form': form})
