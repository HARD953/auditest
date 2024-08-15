from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
from custumer.models import*
from custumer.serializers import UserSerializer1
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .permissions import *
from datetime import datetime

from .importdata import *

class DonneeCollecteeCreate(generics.CreateAPIView):
    queryset = DonneeCollectee.objects.all()
    serializer_class = DonneeCollecteeSerializer1
    
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        # Associer l'utilisateur connecté comme propriétaire du Bien
        if self.request.user.is_anonymous:
            serializer.save()
            # importer_donnees_de_excel("data.xlsx")
        else:
            # importer_donnees_de_excel("data.xlsx")
            serializer.save(agent=self.request.user)

class DonneeCollecteeListAgent(generics.ListAPIView):
    
    serializer_class = DonneeCollecteeSerializer # Assurez-vous que l'utilisateur est authentifié
    
    def get_queryset(self):
        # Filtrer les objets DonneeCollectee pour l'utilisateur connecté et l'entreprise associée
        user = self.request.user
        current_date = datetime.now().date()
        return DonneeCollectee.objects.filter(agent=user,is_deleted="False")
    
class DonneeCollecteeDetailView1(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DonneeCollecteeSerializer
    def get_queryset(self):
        return DonneeCollectee.objects.all()
        
class DonneeCollecteeListAll(generics.ListAPIView):
    permission_classes = [IsAuthenticated] 
    serializer_class = DonneeCollecteeSerializer# Assurez-vous que l'utilisateur est authentifié
    def get_queryset(self):
        # Filtrer les objets DonneeCollectee pour l'utilisateur connecté et l'entreprise associée
        user = self.request.user
        return DonneeCollectee.objects.filter(agent=user,is_deleted="False")

class Allcollecte(generics.ListAPIView):
    permission_classes = [IsAuthenticated] 
    serializer_class = DonneeCollecteeSerializer# Assurez-vous que l'utilisateur est authentifié
    def get_queryset(self):
        # Filtrer les objets DonneeCollectee pour l'utilisateur connecté et l'entreprise associée
        user = self.request.user
        return DonneeCollectee.objects.filter(agent=user,is_deleted="False")

           
# class DonneeCollecteeDetailView(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = DonneeCollecteeSerializer
#     def get_queryset(self):
#         return DonneeCollectee.objects.all()
        
class NombreSupportsParAgent(APIView):
    def get(self, request):
        # Vérifiez si l'utilisateur est authentifié
        if not request.user.is_authenticated:
            return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)

        # Obtenez le nombre de supports collectés par agent
        supports_par_agent = DonneeCollectee.objects.filter(agent=request.user).values('agent').annotate(nombre_supports=Count('id'))

        # supports_par_agent est maintenant une liste de dictionnaires avec 'agent' et 'nombre_supports'
        for entry in supports_par_agent:
            agent = entry['agent']
            nombre_supports = entry['nombre_supports']
            return Response({'agent': agent, 'nombre_supports': nombre_supports}, status=status.HTTP_200_OK)
        

class DonneeCollecteeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DonneeCollectee.objects.filter(is_deleted=False)
    serializer_class = DonneeCollecteeSerializer
    # permission_classes = [permissions.DjangoModelPermissions]
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()  # Récupérer l'instance à mettre à jour
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            # Gérer les images
            if 'image_support' in request.FILES:
                # Supprimer l'ancienne image si nécessaire
                if instance.image_support:
                    instance.image_support.delete()

                # Enregistrer la nouvelle image
                instance.image_support = request.FILES['image_support']

            # Enregistrer les autres données mises à jour
            updated_instance = serializer.save()

            # Répondre avec les données mises à jour
            return Response(self.get_serializer(updated_instance).data)
        else:
            # En cas d'erreurs de validation
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        

class SupportPublicitaireListView(generics.ListCreateAPIView):
    # permission_classes = [IsLanfia] 
    queryset = SupportPublicitaire.objects.all()
    serializer_class = SupportPublicitaireSerializer

class SupportPublicitaireDetailView(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [IsLanfia] 
    queryset = SupportPublicitaire.objects.all()
    serializer_class = SupportPublicitaireSerializer

class MarqueListView(generics.ListCreateAPIView):
    # permission_classes = [IsLanfia]
    queryset = Marque.objects.all()
    serializer_class = MarqueSerializer

class MarqueListViewD(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [IsLanfia]
    queryset = Marque.objects.all()
    serializer_class = MarqueSerializer

class VisibiliteListView(generics.ListCreateAPIView):
    # permission_classes = [IsLanfia]
    queryset = Visibilite.objects.all()
    serializer_class = VisibiliteSerializer

class VisibiliteListViewD(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [IsLanfia]
    queryset = Visibilite.objects.all()
    serializer_class = VisibiliteSerializer

class EtatListView(generics.ListCreateAPIView):
    # permission_classes = [IsLanfia]
    queryset = Etat.objects.all()
    serializer_class = EtatSerializer

class EtatListViewD(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [IsLanfia]
    queryset = Etat.objects.all()
    serializer_class = EtatSerializer

class CanalListView(generics.ListCreateAPIView):
    # permission_classes = [IsLanfia]
    queryset = Canal.objects.all()
    serializer_class = CanalSerializer

class CanalListViewD(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [IsLanfia]
    queryset = Canal.objects.all()
    serializer_class = CanalSerializer

class SiteListView(generics.ListCreateAPIView):
    # permission_classes = [IsLanfia]
    queryset = Site.objects.all()
    serializer_class = SiteSerializer

class SiteListViewD(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [IsLanfia]
    queryset = Site.objects.all()
    serializer_class = SiteSerializer

class CommuneL(generics.ListCreateAPIView):
    # permission_classes = [IsLanfia]
    queryset = Commune.objects.all()
    serializer_class = CommuneSerializers

class CommuneDetail(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [IsLanfia]
    queryset = Commune.objects.all()
    serializer_class = CommuneSerializers

class CommuneApp(generics.ListAPIView):
    # permission_classes = [IsLanfia]
    queryset = Commune.objects.all()
    serializer_class = CommuneSerializersApp




from django.db.models import Q

class DonneeCollecteeList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DonneeCollecteeSerializer

    def get_queryset(self):
        user = self.request.user
        # Récupérer les paramètres de date de début et de fin depuis les paramètres d'URL
        start_date_str = self.kwargs.get('start_date')
        end_date_str = self.kwargs.get('end_date')

        # Convertir les chaînes de date en objets datetime.date si elles sont fournies
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else None
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None

        # Récupérer le queryset de tous les objets DonneeCollectee
        queryset = DonneeCollectee.objects.filter(is_deleted="False")

        # Filtrer le queryset en fonction des dates fournies
        if start_date and end_date:
            queryset = queryset.filter(create__date__range=(start_date, end_date))
        elif start_date:
            queryset = queryset.filter(create__date__gte=start_date)
        elif end_date:
            queryset = queryset.filter(create__date__lte=end_date)
        
        # Créer un dictionnaire de filtres pour les autres champs
        filters_dict = {
            'entreprise': 'MTN CI',
            'Marque': 'MTN CI',
            'commune': 'cocody',
            'quartier': '',
            'type_support': 'Affiche',
            'canal': 'franchise',
            'etat_support': 'Bon',
            'typesite': '',
            'visibilite': 'Bonne',
            'duree': '12',
            'surface': '4'
        }

        # Créer un dictionnaire de correspondance entre les noms de champ dans le modèle DonneeCollectee
        # et les noms de champ attendus dans le dictionnaire de filtres
        field_mapping = {
            'entreprise': 'entreprise',
            'Marque': 'Marque',
            'commune': 'commune',
            'quartier': 'quartier',
            'type_support': 'type_support',
            'canal': 'canal',
            'etat_support': 'etat_support',
            'typesite': 'typesite',
            'visibilite': 'visibilite',
            'anciennete': 'anciennete',
            'duree': 'duree',
            'surface': 'surface'
        }
        # Appliquer les filtres dynamiquement en parcourant le dictionnaire de filtres
        for key, value in filters_dict.items():
            if key in field_mapping:
                field_name = field_mapping[key]
                # Construire le filtre pour ce champ spécifique avec icontains
                queryset = queryset.filter(**{f'{field_name}__icontains': value})
        if user.is_agent:
            return queryset
        else:
            return queryset.filter(entreprise=user.entreprise)
        

# from rest_framework import generics
# from .models import DonneeCollectee
# from .serializers import DonneeCollecteeSerializer
# from django.http import JsonResponse

# class DonneeCollecteeList(generics.GenericAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = DonneeCollecteeSerializer

#     def post(self, request, *args, **kwargs):
#         user = request.user
#         queryset = DonneeCollectee.objects.filter(is_deleted="False")

#         # Récupérer les données POST envoyées avec la requête
#         filters_dict = request.data

#         # Récupérer les paramètres de date de début et de fin
#         start_date_str = filters_dict.get('start_date')
#         end_date_str = filters_dict.get('end_date')

#         # Convertir les chaînes de date en objets datetime.date si elles sont fournies
#         start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else None
#         end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None

#         # Filtrer le queryset en fonction des dates fournies
#         if start_date and end_date:
#             queryset = queryset.filter(create__date__range=(start_date, end_date))
#         elif start_date:
#             queryset = queryset.filter(create__date__gte=start_date)
#         elif end_date:
#             queryset = queryset.filter(create__date__lte=end_date)

#         # Créer un dictionnaire de correspondance entre les noms de champ dans le modèle DonneeCollectee
#         # et les noms de champ attendus dans le dictionnaire de filtres
        
#         field_mapping = {
#             'entreprise': 'entreprise',
#             'Marque': 'Marque',
#             'commune': 'commune',
#             'ville': 'ville',
#             'quartier': 'quartier',
#             'type_support': 'type_support',
#             'canal': 'canal',
#             'etat_support': 'etat_support',
#             'typesite': 'typesite',
#             'visibilite': 'visibilite',
#             'anciennete': 'anciennete',
#             'duree': 'duree',
#             'surface': 'surface'
#         }

#         # Appliquer les filtres dynamiques en parcourant le dictionnaire de filtres
#         for key, value in filters_dict.items():
#             if key in field_mapping and key not in ['start_date', 'end_date']:
#                 field_name = field_mapping[key]
#                 # Construire le filtre pour ce champ spécifique avec icontains
#                 queryset = queryset.filter(**{f'{field_name}__icontains': value})

#         # Appliquer le filtre supplémentaire pour l'utilisateur non-agent
#         if not user.is_agent:
#             queryset = queryset.filter(entreprise=user.entreprise)

#         # Sérialiser le queryset filtré
#         serializer = self.serializer_class(queryset, many=True)
#         return JsonResponse(serializer.data, safe=False)


from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .models import DonneeCollectee
from .serializers import DonneeCollecteeSerializer
from django.http import JsonResponse
from datetime import datetime

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 200

class DonneeCollecteeList(generics.GenericAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = DonneeCollecteeSerializer
    pagination_class = StandardResultsSetPagination

    def post(self, request, *args, **kwargs):
        # user = request.user
        queryset = DonneeCollectee.objects.all()

        # Récupérer les données POST envoyées avec la requête
        filters_dict = request.data

        # Récupérer les paramètres de date de début et de fin
        start_date_str = filters_dict.get('start_date')
        end_date_str = filters_dict.get('end_date')

        # Convertir les chaînes de date en objets datetime.date si elles sont fournies
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else None
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None

        # Filtrer le queryset en fonction des dates fournies
        if start_date and end_date:
            queryset = queryset.filter(create__date__range=(start_date, end_date))
        elif start_date:
            queryset = queryset.filter(create__date__gte=start_date)
        elif end_date:
            queryset = queryset.filter(create__date__lte=end_date)

        # Créer un dictionnaire de correspondance entre les noms de champ dans le modèle DonneeCollectee
        # et les noms de champ attendus dans le dictionnaire de filtres
        field_mapping = {
            'entreprise': 'entreprise',
            'Marque': 'Marque',
            'commune': 'commune',
            'ville': 'ville',
            'quartier': 'quartier',
            'type_support': 'type_support',
            'canal': 'canal',
            'etat_support': 'etat_support',
            'typesite': 'typesite',
            'visibilite': 'visibilite',
            'anciennete': 'anciennete',
            'duree': 'duree',
            'surface': 'surface'
        }

        # Appliquer les filtres dynamiques en parcourant le dictionnaire de filtres
        for key, value in filters_dict.items():
            if key in field_mapping and key not in ['start_date', 'end_date']:
                field_name = field_mapping[key]
                # Construire le filtre pour ce champ spécifique avec icontains
                queryset = queryset.filter(**{f'{field_name}__icontains': value})

        # Appliquer le filtre supplémentaire pour l'utilisateur non-agent
        # if not user.is_agent:
        #     queryset = queryset.filter(entreprise=user.entreprise)

        # Pagination des résultats
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)

        # Sérialiser le queryset paginé
        serializer = self.serializer_class(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)
