from django.contrib import admin
from .models import Arbeitsprobe, Script

@admin.register(Arbeitsprobe)
class ArbeitsprobeAdmin(admin.ModelAdmin):
    list_display = ['auftrag', 'generated_title', 'quality', 'api_kosten', 'erstellt_am']
    list_filter = ['quality', 'erstellt_am']
    search_fields = ['generated_title', 'content', 'auftrag__id', 'auftrag__titel']
    readonly_fields = ['erstellt_am', 'api_kosten']
    list_editable = ['quality']

    fieldsets = (
        ('Auftrag & Titel', {
            'fields': ('auftrag', 'generated_title'),
            'description': 'OFFENER Workflow: Titel wird GENERIERT, KEINE Serper API'
        }),
        ('Inhalt & Qualität', {
            'fields': ('content', 'quality')
        }),
        ('Upwork Integration', {
            'fields': ('upwork_job_url', 'upwork_job_description'),
            'classes': ('collapse',)
        }),
        ('Tracking', {
            'fields': ('erstellt_am', 'api_kosten'),
            'classes': ('collapse',)
        })
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('auftrag')

    def save_model(self, request, obj, form, change):
        # API-Kosten automatisch setzen
        obj.api_kosten = obj.get_api_cost()
        super().save_model(request, obj, form, change)

        self.message_user(request, f"Arbeitsprobe für OFFENEN Auftrag erstellt. API-Kosten: ${obj.api_kosten}")


@admin.register(Script)
class ScriptAdmin(admin.ModelAdmin):
    list_display = ['auftrag', 'kunde_title', 'week_number', 'script_status', 'serper_api_calls', 'serper_kosten', 'erstellt_am']
    list_filter = ['script_status', 'week_number', 'erstellt_am']
    search_fields = ['kunde_title', 'content', 'auftrag__id', 'auftrag__titel']
    readonly_fields = ['erstellt_am', 'serper_api_calls', 'serper_kosten']
    list_editable = ['script_status', 'week_number']

    fieldsets = (
        ('Auftrag & Kunde-Titel', {
            'fields': ('auftrag', 'kunde_title'),
            'description': 'AKTIVER Workflow: Titel vom KUNDEN vorgegeben, MIT Serper API'
        }),
        ('Inhalt & Status', {
            'fields': ('content', 'script_status', 'week_number')
        }),
        ('Kunde-Briefing', {
            'fields': ('kunde_briefing', 'kunde_keywords'),
            'classes': ('collapse',)
        }),
        ('Research & API', {
            'fields': ('research_data', 'serper_api_calls', 'serper_kosten'),
            'classes': ('collapse',)
        }),
        ('Tracking', {
            'fields': ('erstellt_am',),
            'classes': ('collapse',)
        })
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('auftrag')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        self.message_user(request, f"Script für AKTIVEN Auftrag erstellt. Serper API-Calls: {obj.serper_api_calls}")
