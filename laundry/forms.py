# reservations/forms.py
# from django import forms
# from bootstrap_datepicker_plus.widgets import DatePickerInput
# from .models import Reservation

# class ReservationForm(forms.ModelForm):
#     class Meta:
#         model = Reservation
#         fields = ['date', 'start_time', 'end_time']
#         widgets = {
#             'date': DatePickerInput(format='%Y-%m-%d'),
#             'start_time': forms.TimeInput(attrs={'type': 'time'}),
#             'end_time': forms.TimeInput(attrs={'type': 'time'}),
#         }

# class DateForm(forms.Form):
#     date = forms.DateField(widget=DatePickerInput(format='%Y-%m-%d'))


from django import forms
from bootstrap_datepicker_plus.widgets import DatePickerInput
from .models import Reservation

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['date', 'start_time', 'end_time']
        widgets = {
            'date': DatePickerInput(options={'format': 'YYYY-MM-DD'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

class DateForm(forms.Form):
    date = forms.DateField(widget=DatePickerInput(options={'format': 'YYYY-MM-DD'}))


            