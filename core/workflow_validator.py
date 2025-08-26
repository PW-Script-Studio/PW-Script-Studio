"""
Workflow Validator - Kritische Sicherheitsprüfungen

Stellt sicher, dass die Workflow-Trennung eingehalten wird:
- OFFENE Aufträge: Titel generiert, KEINE Serper API
- AKTIVE Aufträge: Titel vom Kunden, MIT Serper API
"""
import logging

logger = logging.getLogger(__name__)

class WorkflowValidator:
    """
    Validiert und überwacht die korrekte Workflow-Trennung
    """
    
    @staticmethod
    def validate_offen_workflow(auftrag, use_serper=False, generate_title=True):
        """
        Validiert OFFENEN Workflow (Bewerbungen)
        
        Args:
            auftrag: Auftrag-Objekt
            use_serper: Ob Serper API verwendet werden soll
            generate_title: Ob Titel generiert werden soll
        
        Raises:
            ValueError: Bei Workflow-Verletzungen
        """
        if auftrag.status != 'OFFEN':
            raise ValueError(f"Auftrag {auftrag.id} ist nicht OFFEN (Status: {auftrag.status})")
        
        if use_serper:
            raise ValueError(
                f"KRITISCHER FEHLER: Serper API ist für OFFENE Aufträge VERBOTEN! "
                f"Auftrag {auftrag.id} ist eine Bewerbung."
            )
        
        if not generate_title:
            logger.warning(
                f"WARNUNG: Titel sollte für OFFENEN Auftrag {auftrag.id} generiert werden"
            )
        
        logger.info(f"OFFENER Workflow validiert für Auftrag {auftrag.id}")
        return True
    
    @staticmethod
    def validate_aktiv_workflow(auftrag, kunde_title=None, use_serper=True):
        """
        Validiert AKTIVEN Workflow (Kundenprojekte)
        
        Args:
            auftrag: Auftrag-Objekt
            kunde_title: Vom Kunden vorgegebener Titel
            use_serper: Ob Serper API verwendet werden soll
        
        Raises:
            ValueError: Bei Workflow-Verletzungen
        """
        if auftrag.status != 'AKTIV':
            raise ValueError(f"Auftrag {auftrag.id} ist nicht AKTIV (Status: {auftrag.status})")
        
        if not kunde_title:
            raise ValueError(
                f"KRITISCHER FEHLER: Kunde-Titel ist für AKTIVE Aufträge erforderlich! "
                f"Auftrag {auftrag.id} ist ein Kundenprojekt."
            )
        
        if not use_serper:
            logger.warning(
                f"WARNUNG: Serper API sollte für AKTIVEN Auftrag {auftrag.id} verwendet werden"
            )
        
        logger.info(f"AKTIVER Workflow validiert für Auftrag {auftrag.id}")
        return True
    
    @staticmethod
    def get_workflow_requirements(auftrag_status):
        """
        Gibt die Anforderungen für einen Workflow zurück
        
        Returns:
            dict mit Workflow-Anforderungen
        """
        if auftrag_status == 'OFFEN':
            return {
                'workflow_type': 'OFFEN',
                'description': 'Bewerbungen',
                'title_source': 'GENERIERT',
                'serper_api': False,
                'openrouter_api': True,
                'quality_levels': ['bronze', 'silber', 'gold'],
                'cost_range': '$0.35 - $0.93'
            }
        elif auftrag_status == 'AKTIV':
            return {
                'workflow_type': 'AKTIV',
                'description': 'Kundenprojekte',
                'title_source': 'VOM_KUNDEN',
                'serper_api': True,
                'openrouter_api': True,
                'organization': 'WÖCHENTLICH',
                'research_required': True
            }
        else:
            return {
                'workflow_type': 'UNBEKANNT',
                'description': 'Unbekannter Status',
                'error': f'Status {auftrag_status} nicht unterstützt'
            }
    
    @staticmethod
    def log_workflow_action(auftrag, action, details=None):
        """
        Loggt Workflow-Aktionen für Audit-Zwecke
        """
        log_message = f"Workflow-Aktion: {action} für Auftrag {auftrag.id} ({auftrag.status})"
        if details:
            log_message += f" - Details: {details}"
        
        logger.info(log_message)
        
        # Hier könnte zusätzlich in eine Audit-Tabelle geschrieben werden
        return log_message
