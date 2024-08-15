from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Sum
from django.db.models.functions import TruncDate
from django.db.models import FloatField
from django.db.models.functions import Cast
from .models import DonneeCollectee
from datetime import datetime

class GTotalCollectedDataView(APIView):
    def get(self, request, start_date=None, end_date=None):
        # Convertir les dates en objets date si elles sont fournies
        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

        # Définir les filtres de date en fonction des paramètres fournis
        date_filters = {}
        if start_date:
            date_filters['create__date__gte'] = start_date
        if end_date:
            date_filters['create__date__lte'] = end_date

        # Agrégations sur l'ensemble des données collectées
        total_aggregations = {}
        if self.request.user.is_agent:
            for etat_support in ['Bon', 'Défraichis', 'Détérioré']:
                etat_aggregations = DonneeCollectee.objects.filter(
                    etat_support=etat_support, **date_filters,is_deleted="False"
                ).annotate(
                    date=TruncDate('create')
                ).values('date').annotate(
                    nombre_total=Count('id'),
                    montant_total_tsp=Sum(Cast('TSP', FloatField())),
                    montant_total_odp=Sum(Cast('ODP_value', FloatField())),
                    montant_total=Sum(Cast('TSP', FloatField())) + Sum(Cast('ODP_value', FloatField()))
                )

                # Ajouter la somme des montants pour chaque état
                somme_montant_total_tsp = sum(item['montant_total_tsp'] for item in etat_aggregations)
                somme_montant_total_odp = sum(item['montant_total_odp'] for item in etat_aggregations)
                somme_montant_total = sum(item['montant_total'] for item in etat_aggregations)

                total_aggregations[etat_support] = {
                    'somme_montant_total_tsp': somme_montant_total_tsp,
                    'somme_montant_total_odp': somme_montant_total_odp,
                    'somme_montant_total': somme_montant_total,
                    'nombre_total': sum(item['nombre_total'] for item in etat_aggregations),
                }

            # Ajouter une agrégation pour la somme totale sans distinction des états
            total_aggregations['Total'] = DonneeCollectee.objects.filter(
                **date_filters,is_deleted="False"
            ).aggregate(
                somme_montant_total_tsp=Sum(Cast('TSP', FloatField())),
                somme_montant_total_odp=Sum(Cast('ODP_value', FloatField())),
                somme_montant_total=Sum(Cast('TSP', FloatField())) + Sum(Cast('ODP_value', FloatField())),
                nombre_total=Count('id'),
            )
        else:
            for etat_support in ['Bon', 'Défraichis', 'Détérioré']:
                etat_aggregations = DonneeCollectee.objects.filter(
                    entreprise=self.request.user.entreprise,etat_support=etat_support, **date_filters,is_deleted="False"
                ).annotate(
                    date=TruncDate('create')
                ).values('date').annotate(
                    nombre_total=Count('id'),
                    montant_total_tsp=Sum(Cast('TSP', FloatField())),
                    montant_total_odp=Sum(Cast('ODP_value', FloatField())),
                    montant_total=Sum(Cast('TSP', FloatField())) + Sum(Cast('ODP_value', FloatField()))
                )

                # Ajouter la somme des montants pour chaque état
                somme_montant_total_tsp = sum(item['montant_total_tsp'] for item in etat_aggregations)
                somme_montant_total_odp = sum(item['montant_total_odp'] for item in etat_aggregations)
                somme_montant_total = sum(item['montant_total'] for item in etat_aggregations)

                total_aggregations[etat_support] = {
                    'somme_montant_total_tsp': somme_montant_total_tsp,
                    'somme_montant_total_odp': somme_montant_total_odp,
                    'somme_montant_total': somme_montant_total,
                    'nombre_total': sum(item['nombre_total'] for item in etat_aggregations),
                }

            # Ajouter une agrégation pour la somme totale sans distinction des états
            total_aggregations['Total'] = DonneeCollectee.objects.filter(
                entreprise=self.request.user.entreprise,**date_filters,is_deleted="False"
            ).aggregate(
                somme_montant_total_tsp=Sum(Cast('TSP', FloatField())),
                somme_montant_total_odp=Sum(Cast('ODP_value', FloatField())),
                somme_montant_total=Sum(Cast('TSP', FloatField())) + Sum(Cast('ODP_value', FloatField())),
                nombre_total=Count('id'),)
            
        return Response({
            'total_aggregations': total_aggregations,
        }, status=status.HTTP_200_OK)
