"""
Cost Tracker - Überwacht API-Kosten für beide Workflows

Trackt Kosten für:
- OpenRouter API (beide Workflows)
- Serper API (nur aktive Aufträge)
- Qualitätsstufen (Bronze/Silber/Gold)
"""
import logging
from decimal import Decimal
from django.utils import timezone

logger = logging.getLogger(__name__)

class CostTracker:
    """
    Überwacht und trackt API-Kosten
    """
    
    # Kosten-Definitionen
    QUALITY_COSTS = {
        'bronze': Decimal('0.35'),
        'silber': Decimal('0.63'),
        'gold': Decimal('0.93')
    }
    
    SERPER_COST_PER_CALL = Decimal('0.01')
    
    def __init__(self):
        self.session_costs = {
            'openrouter': Decimal('0.00'),
            'serper': Decimal('0.00'),
            'total': Decimal('0.00')
        }
    
    def track_openrouter_cost(self, quality_level, tokens_used=None, actual_cost=None):
        """
        Trackt OpenRouter API Kosten
        
        Args:
            quality_level: bronze/silber/gold
            tokens_used: Anzahl verwendeter Tokens
            actual_cost: Tatsächliche Kosten (falls verfügbar)
        
        Returns:
            Decimal: Kosten für diesen Aufruf
        """
        if actual_cost is not None:
            cost = Decimal(str(actual_cost))
        elif quality_level in self.QUALITY_COSTS:
            cost = self.QUALITY_COSTS[quality_level]
        else:
            logger.warning(f"Unbekannte Qualitätsstufe: {quality_level}")
            cost = Decimal('0.50')  # Fallback
        
        self.session_costs['openrouter'] += cost
        self.session_costs['total'] += cost
        
        logger.info(f"OpenRouter Kosten: ${cost} ({quality_level})")
        return cost
    
    def track_serper_cost(self, api_calls=1, workflow_type=None):
        """
        Trackt Serper API Kosten
        
        Args:
            api_calls: Anzahl API-Aufrufe
            workflow_type: OFFEN oder AKTIV (für Validierung)
        
        Returns:
            Decimal: Kosten für diese Aufrufe
        """
        # Sicherheitscheck: Serper nur für AKTIVE Aufträge
        if workflow_type != 'AKTIV':
            raise ValueError(
                f"FEHLER: Serper API nur für AKTIVE Aufträge erlaubt! "
                f"Workflow: {workflow_type}"
            )
        
        cost = self.SERPER_COST_PER_CALL * api_calls
        self.session_costs['serper'] += cost
        self.session_costs['total'] += cost
        
        logger.info(f"Serper Kosten: ${cost} ({api_calls} Aufrufe)")
        return cost
    
    def get_session_costs(self):
        """
        Gibt die Kosten der aktuellen Session zurück
        """
        return dict(self.session_costs)
    
    def get_quality_cost_estimate(self, quality_level):
        """
        Gibt geschätzte Kosten für eine Qualitätsstufe zurück
        """
        return self.QUALITY_COSTS.get(quality_level, Decimal('0.00'))
    
    def calculate_workflow_cost(self, workflow_type, quality_level=None, serper_calls=0):
        """
        Berechnet geschätzte Kosten für einen Workflow
        
        Args:
            workflow_type: OFFEN oder AKTIV
            quality_level: bronze/silber/gold (für OFFEN)
            serper_calls: Anzahl Serper-Aufrufe (für AKTIV)
        
        Returns:
            dict mit Kosten-Breakdown
        """
        costs = {
            'openrouter': Decimal('0.00'),
            'serper': Decimal('0.00'),
            'total': Decimal('0.00')
        }
        
        if workflow_type == 'OFFEN':
            # Offene Aufträge: Nur OpenRouter, basierend auf Qualität
            if quality_level:
                costs['openrouter'] = self.QUALITY_COSTS.get(
                    quality_level, 
                    Decimal('0.50')
                )
            
        elif workflow_type == 'AKTIV':
            # Aktive Aufträge: OpenRouter (Gold) + Serper
            costs['openrouter'] = self.QUALITY_COSTS['gold']  # Höchste Qualität für Kunden
            costs['serper'] = self.SERPER_COST_PER_CALL * serper_calls
        
        costs['total'] = costs['openrouter'] + costs['serper']
        
        return costs
    
    def log_cost_summary(self, auftrag_id, workflow_type):
        """
        Loggt eine Kosten-Zusammenfassung
        """
        costs = self.get_session_costs()
        
        summary = (
            f"Kosten-Zusammenfassung für Auftrag {auftrag_id} ({workflow_type}):\n"
            f"  OpenRouter: ${costs['openrouter']:.2f}\n"
            f"  Serper: ${costs['serper']:.2f}\n"
            f"  Gesamt: ${costs['total']:.2f}"
        )
        
        logger.info(summary)
        return summary
    
    def reset_session(self):
        """
        Setzt die Session-Kosten zurück
        """
        self.session_costs = {
            'openrouter': Decimal('0.00'),
            'serper': Decimal('0.00'),
            'total': Decimal('0.00')
        }
        logger.info("Kosten-Session zurückgesetzt")
