# reservations/urls.py
from django.urls import path
from .views import reserve_laundry, show_today, show_selected_day, ShowSelectedDayView
#from . views import show_calendar
app_name = 'laundry'

urlpatterns = [
    path('reserve/', reserve_laundry, name='reserve_laundry'),
    path('show_today/', show_today, name='show_today'),
    path('show_selected_day/', show_selected_day, name='show_selected_day'),
    # path('cal/', show_calendar, name='show_calendar'),
    # path('calendar/<int:year>/<int:month>/', show_calendar, name='show_calendar'),
    path('show_selected_dayy/', ShowSelectedDayView.as_view(), name='show_selected_dayy'),
]
