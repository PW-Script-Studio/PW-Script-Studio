"""
PW-Script-Studio URL Configuration

Hauptrouting für das Script-Management-System mit 3 Kacheln:
- Kachel 1: Auftragsverwaltung
- Kachel 2: Analyse (getrennte Workflows für OFFEN/AKTIV)
- Kachel 3: Export
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Dashboard (Hauptseite)
    path('', include('apps.dashboard.urls')),

    # Kachel 1: Auftragsverwaltung
    path('kachel1/', include('apps.kachel1_auftragsverwaltung.urls')),

    # Kachel 2: Analyse (mit getrennten Workflows)
    path('kachel2/', include('apps.kachel2_analyse.urls')),

    # Kachel 3: Export
    path('kachel3/', include('apps.kachel3_export.urls')),

    # API Endpoints
    path('api/', include('apps.api.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
