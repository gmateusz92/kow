# reservations/urls.py
from django.urls import path
# from .views import reserve_laundry, show_schedule, show_selected_day, show_calendar
from . views import show_calendar
app_name = 'laundry'

urlpatterns = [
    # path('reserve/', reserve_laundry, name='reserve_laundry'),
    # path('schedule/', show_schedule, name='schedule'),
    # path('show_selected_day/', show_selected_day, name='show_selected_day'),
    path('cal/', show_calendar, name='show_calendar'),
    path('calendar/<int:year>/<int:month>/', show_calendar, name='show_calendar'),
]
