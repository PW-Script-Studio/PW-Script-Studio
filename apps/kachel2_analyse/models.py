from django.db import models
from apps.kachel1_auftragsverwaltung.models import Auftrag

class Arbeitsprobe(models.Model):
    """
    Model für OFFENE Aufträge (Bewerbungen)
    - Titel wird GENERIERT (nicht vom Kunden vorgegeben)
    - KEINE Serper API Nutzung
    - Fokus auf Qualitätsstufen (Bronze/Silber/Gold)
    """
    QUALITY_CHOICES = [
        ('bronze', 'Bronze ($0.35)'),
        ('silber', 'Silber ($0.63)'),
        ('gold', 'Gold ($0.93)'),
    ]

    auftrag = models.ForeignKey(
        Auftrag,
        on_delete=models.CASCADE,
        limit_choices_to={'status': 'OFFEN'},
        related_name='arbeitsproben'
    )

    # GENERIERTER Titel (nicht vom Kunden!)
    generated_title = models.CharField(
        max_length=200,
        help_text="Automatisch generierter Titel für die Arbeitsprobe"
    )

    content = models.TextField(help_text="Generierter Inhalt der Arbeitsprobe")
    quality = models.CharField(
        max_length=10,
        choices=QUALITY_CHOICES,
        help_text="Qualitätsstufe bestimmt API-Kosten"
    )

    # Upwork-spezifische Felder
    upwork_job_url = models.URLField(blank=True, null=True)
    upwork_job_description = models.TextField(blank=True)

    # Tracking
    erstellt_am = models.DateTimeField(auto_now_add=True)
    api_kosten = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    class Meta:
        verbose_name = "Arbeitsprobe"
        verbose_name_plural = "Arbeitsproben"
        ordering = ['-erstellt_am']

    def __str__(self):
        return f"{self.auftrag.id} - {self.generated_title} ({self.quality})"

    def get_api_cost(self):
        """Berechnet API-Kosten basierend auf Qualität"""
        costs = {
            'bronze': 0.35,
            'silber': 0.63,
            'gold': 0.93
        }
        return costs.get(self.quality, 0.00)


class Script(models.Model):
    """
    Model für AKTIVE Aufträge (Kundenprojekte)
    - Titel wird vom KUNDEN vorgegeben (nicht generiert!)
    - MIT Serper API für Research
    - Fokus auf wöchentliche Organisation
    """
    auftrag = models.ForeignKey(
        Auftrag,
        on_delete=models.CASCADE,
        limit_choices_to={'status': 'AKTIV'},
        related_name='scripts'
    )

    # VOM KUNDEN vorgegebener Titel (nicht generiert!)
    kunde_title = models.CharField(
        max_length=200,
        help_text="Vom Kunden vorgegebener Titel - NICHT generieren!"
    )

    # Serper API Research Daten
    research_data = models.JSONField(
        default=dict,
        help_text="Research-Daten von Serper API"
    )

    content = models.TextField(help_text="Generierter Script-Inhalt")

    # Wöchentliche Organisation
    week_number = models.IntegerField(help_text="Wochennummer für Organisation")

    # Kunde-spezifische Felder
    kunde_briefing = models.TextField(blank=True, help_text="Briefing vom Kunden")
    kunde_keywords = models.TextField(blank=True, help_text="Keywords vom Kunden")

    # Tracking
    erstellt_am = models.DateTimeField(auto_now_add=True)
    serper_api_calls = models.IntegerField(default=0, help_text="Anzahl Serper API Aufrufe")
    serper_kosten = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    # Status für Script-Entwicklung
    STATUS_CHOICES = [
        ('RESEARCH', 'Research Phase'),
        ('DRAFT', 'Entwurf'),
        ('REVIEW', 'Review'),
        ('FINAL', 'Final'),
        ('DELIVERED', 'Ausgeliefert'),
    ]
    script_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='RESEARCH'
    )

    class Meta:
        verbose_name = "Script"
        verbose_name_plural = "Scripts"
        ordering = ['-week_number', '-erstellt_am']

    def __str__(self):
        return f"{self.auftrag.id} - {self.kunde_title} (Woche {self.week_number})"

    def add_serper_call(self, cost=0.01):
        """Trackt Serper API Aufrufe und Kosten"""
        self.serper_api_calls += 1
        self.serper_kosten += cost
        self.save()
