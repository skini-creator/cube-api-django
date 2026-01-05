from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Plat, Role, CustomUser

User = get_user_model()

# --- SÉRIALISEUR UTILISATEUR (AUTHENTIFICATION) ---

class UserSerializer(serializers.ModelSerializer):
    # Champ rôle en lecture seule pour éviter que l'utilisateur le change
    role = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'role', 'is_active', 'is_staff']
        extra_kwargs = {'password': {'write_only': True}} # Le mot de passe ne doit jamais être renvoyé

    def create(self, validated_data):
        # Récupère le mot de passe avant de le retirer
        password = validated_data.pop('password', None)
        
        # Le rôle par défaut est 'CLIENT' si non spécifié.
        # Nous allons forcer le rôle à CLIENT ici pour l'enregistrement public
        validated_data['role'] = Role.CLIENT
        
        # Crée une instance de l'utilisateur CustomUser
        instance = self.Meta.model(**validated_data)
        
        # Définit le mot de passe haché si un mot de passe a été fourni
        if password is not None:
            instance.set_password(password)
        
        instance.save()
        return instance

    def update(self, instance, validated_data):
        # Gère la modification du mot de passe si le champ 'password' est présent
        password = validated_data.pop('password', None)
        if password is not None:
            instance.set_password(password)
            
        return super().update(instance, validated_data)


# --- SÉRIALISEUR PLAT (GÉRÉ PAR L'ADMIN) ---

class PlatSerializer(serializers.ModelSerializer):
    # Affiche l'email de l'auteur (l'administrateur qui a ajouté le plat)
    auteur_email = serializers.ReadOnlyField(source='auteur.email')

    class Meta:
        model = Plat
        fields = ['id', 'nom', 'description', 'prix', 'disponible', 'auteur', 'auteur_email', 'date_creation']
        read_only_fields = ['auteur'] # L'auteur est défini dans la vue (perform_create)