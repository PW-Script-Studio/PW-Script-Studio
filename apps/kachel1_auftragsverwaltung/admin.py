from django.contrib import admin
from .models import Auftrag

@admin.register(Auftrag)
class AuftragAdmin(admin.ModelAdmin):
    list_display = ['id', 'titel', 'status', 'prioritaet', 'woche', 'erstellt_am']
    list_filter = ['status', 'prioritaet', 'woche', 'erstellt_am']
    search_fields = ['id', 'titel', 'beschreibung']
    readonly_fields = ['erstellt_am', 'aktualisiert_am']
    list_editable = ['status', 'prioritaet', 'woche']

    fieldsets = (
        ('Basis Information', {
            'fields': ('id', 'titel', 'beschreibung')
        }),
        ('Status & Organisation', {
            'fields': ('status', 'prioritaet', 'woche')
        }),
        ('Zeitstempel', {
            'fields': ('erstellt_am', 'aktualisiert_am'),
            'classes': ('collapse',)
        })
    )

    def get_queryset(self, request):
        """Zeigt Workflow-Trennung in der Liste"""
        qs = super().get_queryset(request)
        return qs.select_related()

    def save_model(self, request, obj, form, change):
        """Validiert Workflow-Logik beim Speichern"""
        super().save_model(request, obj, form, change)

        # Info-Message für Workflow
        if obj.is_offen():
            self.message_user(request, f"OFFENER Auftrag: Titel wird generiert, KEINE Serper API")
        elif obj.is_aktiv():
            self.message_user(request, f"AKTIVER Auftrag: Kunde-Titel, MIT Serper API")
