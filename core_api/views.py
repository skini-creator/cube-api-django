from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model

# Import de nos modèles et sérialiseurs
from .models import Plat
from .serializers import (
    UserSerializer,
    PlatSerializer
)

# --- Permissions Personnalisées ---
class IsAdmin(permissions.BasePermission):
    """
    Permet l'accès uniquement aux utilisateurs ayant le rôle ADMIN.
    """
    def has_permission(self, request, view):
        # Vérifie si l'utilisateur est authentifié et si son rôle est 'ADMIN'
        return request.user.is_authenticated and request.user.role == 'ADMIN'


# --- 1. VUES D'AUTHENTIFICATION ---

class RegisterView(generics.CreateAPIView):
    """
    Endpoint pour l'enregistrement d'un nouvel utilisateur.
    """
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny] 

    def perform_create(self, serializer):
        serializer.save()

# --- 2. VUES DE GESTION DES PLATS (CRUD) ---

class PlatListCreateView(generics.ListCreateAPIView):
    """
    Permet de lister tous les plats (GET) ou de créer un nouveau plat (POST).
    """
    queryset = Plat.objects.all()
    serializer_class = PlatSerializer

    def get_permissions(self):
        """
        Définit les permissions :
        - GET (Liste) : AllowAny (tout le monde)
        - POST (Création) : IsAdmin (seulement l'Admin)
        """
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        # Utilise IsAuthenticated et IsAdmin, car la permission par défaut du projet est IsAuthenticated
        return [permissions.IsAuthenticated(), IsAdmin()] 

    def perform_create(self, serializer):
        serializer.save(auteur=self.request.user)


class PlatRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Permet de récupérer les détails, modifier ou supprimer un plat spécifique.
    """
    queryset = Plat.objects.all()
    serializer_class = PlatSerializer

    def get_permissions(self):
        """
        Définit les permissions :
        - GET (Détail) : AllowAny (tout le monde)
        - PUT/PATCH/DELETE : IsAdmin (seulement l'Admin)
        """
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), IsAdmin()]