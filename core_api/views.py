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
# Cette classe assure que seul un utilisateur ayant le rôle 'ADMIN' peut accéder.
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
    Utilise le sérialiseur UserSerializer pour valider les données et créer un utilisateur.
    """
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny] # Tout le monde peut s'enregistrer

    def perform_create(self, serializer):
        # La méthode create du UserSerializer gère le hashage du mot de passe
        serializer.save()

# Note : Les vues pour la connexion (Login) et la déconnexion (Logout) seront 
# implémentées en utilisant Simple JWT plus tard, après avoir installé le package.


# --- 2. VUES DE GESTION DES PLATS (CRUD) ---

# Gère les requêtes GET (liste) et POST (création)
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
        return [permissions.IsAuthenticated(), IsAdmin()] # Exige l'authentification ET le rôle ADMIN

    def perform_create(self, serializer):
        # Sauvegarde le plat en liant l'administrateur qui l'a créé
        serializer.save(auteur=self.request.user)


# Gère les requêtes GET (détail), PUT/PATCH (modification), et DELETE (suppression)
class PlatRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Permet de récupérer les détails, modifier ou supprimer un plat spécifique.
    """
    queryset = Plat.objects.all()
    serializer_class = PlatSerializer
    # Le lookup_field par défaut est 'pk' (ID), ce qui est suffisant.

    def get_permissions(self):
        """
        Définit les permissions :
        - GET (Détail) : AllowAny (tout le monde)
        - PUT/PATCH/DELETE : IsAdmin (seulement l'Admin)
        """
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), IsAdmin()] # Exige l'authentification ET le rôle ADMIN