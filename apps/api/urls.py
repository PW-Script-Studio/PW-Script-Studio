from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuftragViewSet, ArbeitsprobeViewSet, ScriptViewSet

app_name = 'api'

# Router für REST API Endpoints
router = DefaultRouter()
router.register(r'auftraege', AuftragViewSet, basename='auftrag')
router.register(r'arbeitsproben', ArbeitsprobeViewSet, basename='arbeitsprobe')
router.register(r'scripts', ScriptViewSet, basename='script')

urlpatterns = [
    # REST API Endpoints
    path('', include(router.urls)),

    # DRF Authentication
    path('auth/', include('rest_framework.urls')),
]
