# reservations/urls.py
from django.urls import path
from .views import reserve_laundry, show_schedule,show_schedule_by_day

app_name = 'laundry'

urlpatterns = [
    path('reserve/', reserve_laundry, name='reserve_laundry'),
    path('schedule/', show_schedule, name='schedule'),
    path('schedule/<str:day_of_week>/', show_schedule_by_day, name='show_schedule_by_day'),
]
