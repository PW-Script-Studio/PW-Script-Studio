from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from .models import Auftrag
from core.workflow_validator import WorkflowValidator

def auftrag_list(request):
    """
    Liste aller Aufträge mit Filterung nach Status
    """
    status_filter = request.GET.get('status', 'all')

    if status_filter == 'all':
        auftraege = Auftrag.objects.all()
    else:
        auftraege = Auftrag.objects.filter(status=status_filter.upper())

    auftraege = auftraege.order_by('-erstellt_am')

    context = {
        'auftraege': auftraege,
        'status_filter': status_filter,
        'status_choices': Auftrag.STATUS_CHOICES,
        'page_title': 'Auftragsverwaltung'
    }

    return render(request, 'kachel1/index.html', context)

def auftrag_detail(request, auftrag_id):
    """
    Detailansicht eines Auftrags mit Workflow-Informationen
    """
    auftrag = get_object_or_404(Auftrag, id=auftrag_id)

    # Workflow-Anforderungen abrufen
    workflow_requirements = WorkflowValidator.get_workflow_requirements(auftrag.status)

    context = {
        'auftrag': auftrag,
        'workflow_requirements': workflow_requirements,
        'page_title': f'Auftrag {auftrag.id}'
    }

    return render(request, 'kachel1/auftrag_detail.html', context)

def auftrag_create(request):
    """
    Erstellt neuen Auftrag
    """
    if request.method == 'POST':
        # Hier würde normalerweise ein Form verwendet
        # Für jetzt einfache Implementierung
        messages.info(request, 'Auftrag-Erstellung noch nicht implementiert')
        return redirect('kachel1_auftragsverwaltung:auftrag_list')

    return render(request, 'kachel1/auftrag_create.html')

def auftrag_edit(request, auftrag_id):
    """
    Bearbeitet bestehenden Auftrag
    """
    auftrag = get_object_or_404(Auftrag, id=auftrag_id)

    if request.method == 'POST':
        messages.info(request, 'Auftrag-Bearbeitung noch nicht implementiert')
        return redirect('kachel1_auftragsverwaltung:auftrag_detail', auftrag_id=auftrag.id)

    context = {
        'auftrag': auftrag,
        'page_title': f'Auftrag {auftrag.id} bearbeiten'
    }

    return render(request, 'kachel1/auftrag_edit.html', context)

def auftrag_delete(request, auftrag_id):
    """
    Löscht Auftrag (mit Bestätigung)
    """
    auftrag = get_object_or_404(Auftrag, id=auftrag_id)

    if request.method == 'POST':
        auftrag.delete()
        messages.success(request, f'Auftrag {auftrag_id} wurde gelöscht')
        return redirect('kachel1_auftragsverwaltung:auftrag_list')

    context = {
        'auftrag': auftrag,
        'page_title': f'Auftrag {auftrag.id} löschen'
    }

    return render(request, 'kachel1/auftrag_delete.html', context)
