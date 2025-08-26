from django.urls import path
from . import views

app_name = 'kachel3_export'

urlpatterns = [
    path('', views.export_dashboard, name='export_dashboard'),
    path('pdf/<str:auftrag_id>/', views.export_pdf, name='export_pdf'),
    path('docx/<str:auftrag_id>/', views.export_docx, name='export_docx'),
    path('html/<str:auftrag_id>/', views.export_html, name='export_html'),
]
