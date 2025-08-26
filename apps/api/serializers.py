from rest_framework import serializers
from apps.kachel1_auftragsverwaltung.models import Auftrag
from apps.kachel2_analyse.models import Arbeitsprobe, Script


class AuftragSerializer(serializers.ModelSerializer):
    """Serializer für Auftrag Model"""
    
    # Zusätzliche Felder für Frontend
    is_offen = serializers.ReadOnlyField()
    is_aktiv = serializers.ReadOnlyField()
    arbeitsproben_count = serializers.SerializerMethodField()
    scripts_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Auftrag
        fields = [
            'id', 'titel', 'beschreibung', 'status', 'prioritaet', 'woche',
            'erstellt_am', 'aktualisiert_am', 'is_offen', 'is_aktiv',
            'arbeitsproben_count', 'scripts_count'
        ]
        read_only_fields = ['erstellt_am', 'aktualisiert_am']
    
    def get_arbeitsproben_count(self, obj):
        """Anzahl Arbeitsproben für OFFENE Aufträge"""
        return obj.arbeitsproben.count() if obj.is_offen() else 0
    
    def get_scripts_count(self, obj):
        """Anzahl Scripts für AKTIVE Aufträge"""
        return obj.scripts.count() if obj.is_aktiv() else 0


class ArbeitsprobeSerializer(serializers.ModelSerializer):
    """Serializer für Arbeitsprobe Model (OFFENE Aufträge)"""
    
    auftrag_titel = serializers.CharField(source='auftrag.titel', read_only=True)
    api_cost_calculated = serializers.SerializerMethodField()
    
    class Meta:
        model = Arbeitsprobe
        fields = [
            'id', 'auftrag', 'auftrag_titel', 'generated_title', 'content',
            'quality', 'upwork_job_url', 'upwork_job_description',
            'erstellt_am', 'api_kosten', 'api_cost_calculated'
        ]
        read_only_fields = ['erstellt_am', 'api_kosten']
    
    def get_api_cost_calculated(self, obj):
        """Berechnet API-Kosten basierend auf Qualität"""
        return obj.get_api_cost()
    
    def create(self, validated_data):
        """Automatische API-Kosten-Berechnung beim Erstellen"""
        arbeitsprobe = super().create(validated_data)
        arbeitsprobe.api_kosten = arbeitsprobe.get_api_cost()
        arbeitsprobe.save()
        return arbeitsprobe


class ScriptSerializer(serializers.ModelSerializer):
    """Serializer für Script Model (AKTIVE Aufträge)"""
    
    auftrag_titel = serializers.CharField(source='auftrag.titel', read_only=True)
    
    class Meta:
        model = Script
        fields = [
            'id', 'auftrag', 'auftrag_titel', 'kunde_title', 'content',
            'week_number', 'kunde_briefing', 'kunde_keywords',
            'research_data', 'script_status', 'erstellt_am',
            'serper_api_calls', 'serper_kosten'
        ]
        read_only_fields = ['erstellt_am', 'serper_api_calls', 'serper_kosten']


class DashboardStatsSerializer(serializers.Serializer):
    """Serializer für Dashboard-Statistiken"""
    
    total_auftraege = serializers.IntegerField()
    offene_auftraege = serializers.IntegerField()
    aktive_auftraege = serializers.IntegerField()
    abgeschlossene_auftraege = serializers.IntegerField()
    
    total_arbeitsproben = serializers.IntegerField()
    total_scripts = serializers.IntegerField()
    
    api_kosten_gesamt = serializers.DecimalField(max_digits=10, decimal_places=2)
    serper_kosten_gesamt = serializers.DecimalField(max_digits=10, decimal_places=2)
    
    neueste_auftraege = AuftragSerializer(many=True, read_only=True)
