from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.kachel1_auftragsverwaltung.models import Auftrag

def dashboard_view(request):
    """
    Hauptdashboard mit Übersicht über alle 3 Kacheln
    """
    # Statistiken für Dashboard
    stats = {
        'offene_auftraege': Auftrag.objects.filter(status='OFFEN').count(),
        'aktive_auftraege': Auftrag.objects.filter(status='AKTIV').count(),
        'abgeschlossene_auftraege': Auftrag.objects.filter(status='ABGESCHLOSSEN').count(),
    }

    # Neueste Aufträge
    neueste_auftraege = Auftrag.objects.all().order_by('-erstellt_am')[:5]

    context = {
        'stats': stats,
        'neueste_auftraege': neueste_auftraege,
        'page_title': 'PW-Script-Studio Dashboard'
    }

    return render(request, 'dashboard/dashboard.html', context)
