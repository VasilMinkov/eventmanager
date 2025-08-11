from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('eventmanager.accounts.urls')),
    path('', include('eventmanager.events.urls')),
]
