# reservations/forms.py
from django import forms
from bootstrap_datepicker_plus.widgets import DatePickerInput
from .models import Reservation

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['date', 'start_time', 'end_time']
        widgets = {
            'date': DatePickerInput(format='%Y-%m-%d'),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

class DateForm(forms.Form):
    date = forms.DateField(widget=DatePickerInput(format='%Y-%m-%d'))



class DayOfWeekForm(forms.Form):
    day_of_week = forms.ChoiceField(choices=[
        ('poniedziałek', 'Poniedziałek'),
        ('wtorek', 'Wtorek'),
        ('środa', 'Środa'),
        ('czwartek', 'Czwartek'),
        ('piątek', 'Piątek'),
        ('sobota', 'Sobota'),
        ('niedziela', 'Niedziela'),
    ])
            