from django.urls import path
from . import views

app_name = 'kachel1_auftragsverwaltung'

urlpatterns = [
    path('', views.auftrag_list, name='auftrag_list'),
    path('create/', views.auftrag_create, name='auftrag_create'),
    path('<str:auftrag_id>/', views.auftrag_detail, name='auftrag_detail'),
    path('<str:auftrag_id>/edit/', views.auftrag_edit, name='auftrag_edit'),
    path('<str:auftrag_id>/delete/', views.auftrag_delete, name='auftrag_delete'),
]
