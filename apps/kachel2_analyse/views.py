from django.shortcuts import render
from django.http import JsonResponse

def analyse_dashboard(request):
    """Dashboard für Kachel 2 - Analyse"""
    return render(request, 'kachel2/dashboard.html')

def workflow_offen_list(request):
    """Liste der offenen Workflows (Bewerbungen)"""
    return render(request, 'kachel2/workflow_offen_list.html')

def arbeitsprobe_create(request):
    """Erstelle Arbeitsprobe für offenen Workflow"""
    return render(request, 'kachel2/arbeitsprobe_create.html')

def arbeitsprobe_detail(request, arbeitsprobe_id):
    """Detail einer Arbeitsprobe"""
    return render(request, 'kachel2/arbeitsprobe_detail.html')

def workflow_aktiv_list(request):
    """Liste der aktiven Workflows (Kundenprojekte)"""
    return render(request, 'kachel2/workflow_aktiv_list.html')

def script_create(request):
    """Erstelle Script für aktiven Workflow"""
    return render(request, 'kachel2/script_create.html')

def script_detail(request, script_id):
    """Detail eines Scripts"""
    return render(request, 'kachel2/script_detail.html')

def script_research(request, script_id):
    """Research für Script (nur aktive Workflows)"""
    return render(request, 'kachel2/script_research.html')
