from django.shortcuts import render
from django.http import HttpResponse

def export_dashboard(request):
    """Dashboard für Kachel 3 - Export"""
    return render(request, 'kachel3/dashboard.html')

def export_pdf(request, auftrag_id):
    """Export als PDF"""
    return HttpResponse("PDF Export noch nicht implementiert")

def export_docx(request, auftrag_id):
    """Export als DOCX"""
    return HttpResponse("DOCX Export noch nicht implementiert")

def export_html(request, auftrag_id):
    """Export als HTML"""
    return HttpResponse("HTML Export noch nicht implementiert")
