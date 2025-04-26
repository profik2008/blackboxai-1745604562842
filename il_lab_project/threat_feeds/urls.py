from django.urls import path
from . import views

app_name = 'threat_feeds'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
]
