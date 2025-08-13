from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include('eventmanager.accounts.urls')),
                  path('', include('eventmanager.events.urls')),
                  path('', include('eventmanager.comments.urls')),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
