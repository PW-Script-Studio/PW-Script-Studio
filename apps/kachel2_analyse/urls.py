from django.urls import path, include
from . import views

app_name = 'kachel2_analyse'

urlpatterns = [
    path('', views.analyse_dashboard, name='analyse_dashboard'),
    
    # OFFENE Aufträge (Bewerbungen) - KEINE Serper API
    path('offen/', views.workflow_offen_list, name='workflow_offen_list'),
    path('offen/create/', views.arbeitsprobe_create, name='arbeitsprobe_create'),
    path('offen/<int:arbeitsprobe_id>/', views.arbeitsprobe_detail, name='arbeitsprobe_detail'),
    
    # AKTIVE Aufträge (Kundenprojekte) - MIT Serper API
    path('aktiv/', views.workflow_aktiv_list, name='workflow_aktiv_list'),
    path('aktiv/create/', views.script_create, name='script_create'),
    path('aktiv/<int:script_id>/', views.script_detail, name='script_detail'),
    path('aktiv/<int:script_id>/research/', views.script_research, name='script_research'),
]
