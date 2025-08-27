from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from .services.docraptor_service import DocRaptorService
from apps.kachel2_analyse.models import Arbeitsprobe, Script
from apps.kachel1_auftragsverwaltung.models import Auftrag
import logging

logger = logging.getLogger(__name__)

def export_dashboard(request):
    """Dashboard für Kachel 3 - Export"""
    return render(request, 'kachel3/index.html')

def export_pdf(request, auftrag_id):
    """
    PDF-Export mit DocRaptor
    Unterstützt sowohl Arbeitsproben (OFFENE Aufträge) als auch Scripts (AKTIVE Aufträge)
    """
    try:
        # Typ bestimmen (arbeitsprobe oder script)
        export_type = request.GET.get('type', 'arbeitsprobe')

        logger.info(f"PDF-Export gestartet für Auftrag {auftrag_id}, Typ: {export_type}")

        # Auftrag-Objekt holen für Basis-Informationen
        auftrag = get_object_or_404(Auftrag, id=auftrag_id)

        # Daten je nach Typ holen
        if export_type == 'arbeitsprobe':
            # OFFENER Workflow - Arbeitsprobe
            try:
                probe = Arbeitsprobe.objects.filter(auftrag=auftrag).first()
                if not probe:
                    return HttpResponse("Keine Arbeitsprobe für diesen Auftrag gefunden", status=404)

                data = {
                    'id': auftrag_id,
                    'titel': probe.generated_title,
                    'content': probe.content,
                    'quality': probe.quality,
                    'type': 'Arbeitsprobe (OFFENER Workflow)',
                    'date': probe.erstellt_am.strftime('%d.%m.%Y'),
                    'workflow': 'OFFEN'
                }
            except Exception as e:
                logger.error(f"Fehler beim Laden der Arbeitsprobe: {e}")
                return HttpResponse(f"Fehler beim Laden der Arbeitsprobe: {str(e)}", status=500)

        elif export_type == 'script':
            # AKTIVER Workflow - Script
            try:
                script = Script.objects.filter(auftrag=auftrag).first()
                if not script:
                    return HttpResponse("Kein Script für diesen Auftrag gefunden", status=404)

                data = {
                    'id': auftrag_id,
                    'titel': script.kunde_title,
                    'content': script.content,
                    'quality': 'premium',
                    'type': 'Kunden-Script (AKTIVER Workflow)',
                    'date': script.erstellt_am.strftime('%d.%m.%Y'),
                    'workflow': 'AKTIV'
                }
            except Exception as e:
                logger.error(f"Fehler beim Laden des Scripts: {e}")
                return HttpResponse(f"Fehler beim Laden des Scripts: {str(e)}", status=500)
        else:
            return HttpResponse("Ungültiger Export-Typ", status=400)

        # PDF generieren mit DocRaptor
        try:
            service = DocRaptorService()
            pdf_data = service.generate_pdf(data)

            # Als Download senden
            response = HttpResponse(pdf_data, content_type='application/pdf')
            filename = f"{auftrag_id}_{export_type}.pdf"
            response['Content-Disposition'] = f'attachment; filename="{filename}"'

            logger.info(f"PDF erfolgreich generiert: {filename}")
            return response

        except Exception as e:
            logger.error(f"DocRaptor Fehler: {e}")
            return HttpResponse(f"PDF-Generierung fehlgeschlagen: {str(e)}", status=500)

    except Exception as e:
        logger.error(f"Allgemeiner Fehler beim PDF-Export: {e}")
        return HttpResponse(f"Fehler beim PDF-Export: {str(e)}", status=500)

def export_docx(request, auftrag_id):
    """Export als DOCX - Placeholder für zukünftige Implementierung"""
    return HttpResponse("DOCX Export noch nicht implementiert - verwenden Sie PDF-Export")

def export_html(request, auftrag_id):
    """Export als HTML - Placeholder für zukünftige Implementierung"""
    return HttpResponse("HTML Export noch nicht implementiert - verwenden Sie PDF-Export")
