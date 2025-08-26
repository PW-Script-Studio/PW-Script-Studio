from django.db import models
from django.utils import timezone

class Auftrag(models.Model):
    """
    Hauptmodel für Aufträge - unterscheidet zwischen OFFENEN und AKTIVEN Workflows
    OFFEN = Bewerbungen (generiert Titel, KEINE Serper API)
    AKTIV = Kundenprojekte (Kunde gibt Titel vor, MIT Serper API)
    """
    STATUS_CHOICES = [
        ('OFFEN', 'Offen'),
        ('AKTIV', 'Aktiv'),
        ('ABGESCHLOSSEN', 'Abgeschlossen'),
        ('ABGESAGT', 'Abgesagt'),
    ]

    id = models.CharField(max_length=20, primary_key=True)
    titel = models.CharField(max_length=200)
    beschreibung = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OFFEN')
    erstellt_am = models.DateTimeField(auto_now_add=True)
    aktualisiert_am = models.DateTimeField(auto_now=True)

    # Zusätzliche Felder für bessere Organisation
    woche = models.IntegerField(null=True, blank=True, help_text="Wochennummer für Organisation")
    prioritaet = models.CharField(max_length=10, choices=[
        ('NIEDRIG', 'Niedrig'),
        ('MITTEL', 'Mittel'),
        ('HOCH', 'Hoch'),
    ], default='MITTEL')

    class Meta:
        verbose_name = "Auftrag"
        verbose_name_plural = "Aufträge"
        ordering = ['-erstellt_am']

    def __str__(self):
        return f"{self.id} - {self.titel} ({self.status})"

    def is_offen(self):
        """Prüft ob Auftrag im OFFENEN Workflow ist"""
        return self.status == 'OFFEN'

    def is_aktiv(self):
        """Prüft ob Auftrag im AKTIVEN Workflow ist"""
        return self.status == 'AKTIV'
