from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Count
from apps.kachel1_auftragsverwaltung.models import Auftrag
from apps.kachel2_analyse.models import Arbeitsprobe, Script
from .serializers import (
    AuftragSerializer, ArbeitsprobeSerializer, ScriptSerializer,
    DashboardStatsSerializer
)


class AuftragViewSet(viewsets.ModelViewSet):
    """
    ViewSet für Auftrag Model mit Workflow-spezifischen Endpoints
    """
    queryset = Auftrag.objects.all()
    serializer_class = AuftragSerializer

    @action(detail=False, methods=['get'])
    def offene(self, request):
        """
        Endpoint für OFFENE Aufträge (Bewerbungen)
        - Titel wird GENERIERT
        - KEINE Serper API
        """
        auftraege = Auftrag.objects.filter(status='OFFEN').order_by('-erstellt_am')
        serializer = self.get_serializer(auftraege, many=True)

        return Response({
            'count': auftraege.count(),
            'workflow': 'OFFEN',
            'description': 'Bewerbungen - Titel wird generiert, KEINE Serper API',
            'auftraege': serializer.data
        })

    @action(detail=False, methods=['get'])
    def aktive(self, request):
        """
        Endpoint für AKTIVE Aufträge (Kundenprojekte)
        - Titel vom KUNDEN vorgegeben
        - MIT Serper API
        """
        auftraege = Auftrag.objects.filter(status='AKTIV').order_by('-erstellt_am')
        serializer = self.get_serializer(auftraege, many=True)

        return Response({
            'count': auftraege.count(),
            'workflow': 'AKTIV',
            'description': 'Kundenprojekte - Titel vom Kunden, MIT Serper API',
            'auftraege': serializer.data
        })

    @action(detail=False, methods=['get'])
    def dashboard_stats(self, request):
        """
        Dashboard-Statistiken für Kachel 1
        """
        # Basis-Statistiken
        stats = {
            'total_auftraege': Auftrag.objects.count(),
            'offene_auftraege': Auftrag.objects.filter(status='OFFEN').count(),
            'aktive_auftraege': Auftrag.objects.filter(status='AKTIV').count(),
            'abgeschlossene_auftraege': Auftrag.objects.filter(status='ABGESCHLOSSEN').count(),
            'total_arbeitsproben': Arbeitsprobe.objects.count(),
            'total_scripts': Script.objects.count(),
        }

        # Kosten-Statistiken
        api_kosten = Arbeitsprobe.objects.aggregate(
            total=Sum('api_kosten')
        )['total'] or 0

        serper_kosten = Script.objects.aggregate(
            total=Sum('serper_kosten')
        )['total'] or 0

        stats.update({
            'api_kosten_gesamt': api_kosten,
            'serper_kosten_gesamt': serper_kosten,
        })

        # Neueste Aufträge
        neueste_auftraege = Auftrag.objects.all().order_by('-erstellt_am')[:5]
        stats['neueste_auftraege'] = AuftragSerializer(neueste_auftraege, many=True).data

        serializer = DashboardStatsSerializer(stats)
        return Response(serializer.data)


class ArbeitsprobeViewSet(viewsets.ModelViewSet):
    """
    ViewSet für Arbeitsprobe Model (OFFENE Aufträge)
    """
    queryset = Arbeitsprobe.objects.all()
    serializer_class = ArbeitsprobeSerializer

    def get_queryset(self):
        """Filter nach Auftrag wenn angegeben"""
        queryset = Arbeitsprobe.objects.select_related('auftrag')
        auftrag_id = self.request.query_params.get('auftrag', None)
        if auftrag_id:
            queryset = queryset.filter(auftrag__id=auftrag_id)
        return queryset.order_by('-erstellt_am')

    @action(detail=False, methods=['get'])
    def by_quality(self, request):
        """Arbeitsproben gruppiert nach Qualität"""
        qualities = ['bronze', 'silber', 'gold']
        result = {}

        for quality in qualities:
            arbeitsproben = Arbeitsprobe.objects.filter(quality=quality)
            result[quality] = {
                'count': arbeitsproben.count(),
                'total_cost': arbeitsproben.aggregate(Sum('api_kosten'))['api_kosten__sum'] or 0,
                'arbeitsproben': ArbeitsprobeSerializer(arbeitsproben, many=True).data
            }

        return Response(result)


class ScriptViewSet(viewsets.ModelViewSet):
    """
    ViewSet für Script Model (AKTIVE Aufträge)
    """
    queryset = Script.objects.all()
    serializer_class = ScriptSerializer

    def get_queryset(self):
        """Filter nach Auftrag oder Woche wenn angegeben"""
        queryset = Script.objects.select_related('auftrag')
        auftrag_id = self.request.query_params.get('auftrag', None)
        week_number = self.request.query_params.get('week', None)

        if auftrag_id:
            queryset = queryset.filter(auftrag__id=auftrag_id)
        if week_number:
            queryset = queryset.filter(week_number=week_number)

        return queryset.order_by('-week_number', '-erstellt_am')

    @action(detail=False, methods=['get'])
    def by_week(self, request):
        """Scripts gruppiert nach Wochennummer"""
        scripts_by_week = Script.objects.values('week_number').annotate(
            count=Count('id'),
            total_serper_calls=Sum('serper_api_calls'),
            total_serper_cost=Sum('serper_kosten')
        ).order_by('-week_number')

        return Response(list(scripts_by_week))

    @action(detail=True, methods=['post'])
    def add_serper_call(self, request, pk=None):
        """Serper API Call hinzufügen"""
        script = self.get_object()
        cost = float(request.data.get('cost', 0.01))

        script.add_serper_call(cost)

        return Response({
            'message': 'Serper API Call hinzugefügt',
            'serper_api_calls': script.serper_api_calls,
            'serper_kosten': script.serper_kosten
        })
