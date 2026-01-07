from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Plat, Role # Importe les modèles CustomUser, Plat et Role

# Récupère le modèle utilisateur défini par AUTH_USER_MODEL (CustomUser)
User = get_user_model() 

# --- SÉRIALISEUR UTILISATEUR (AUTHENTIFICATION) ---

class UserSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour l'enregistrement et la gestion des utilisateurs.
    """
    # Le rôle est en lecture seule, car il est attribué côté serveur
    role = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'telephone', 'nom_complet', 'role', 'is_active', 'is_staff']
        # Assure que le mot de passe est uniquement en écriture (n'est jamais renvoyé)
        extra_kwargs = {'password': {'write_only': True}} 

    def create(self, validated_data):
        """
        Crée un nouvel utilisateur en hachant son mot de passe.
        """
        password = validated_data.pop('password', None)
        
        # NOTE : Ici, vous pouvez ajouter la logique pour définir le rôle par défaut (CLIENT)
        # exemple: validated_data['role'] = Role.objects.get(name='CLIENT') 
        # Si vous n'utilisez pas de valeur par défaut, le champ pourrait être null.
        
        instance = self.Meta.model(**validated_data)
        
        if password is not None:
            instance.set_password(password)
        
        instance.save()
        return instance

    def update(self, instance, validated_data):
        """
        Met à jour un utilisateur, gère le hachage si le mot de passe est fourni.
        """
        password = validated_data.pop('password', None)
        if password is not None:
            instance.set_password(password)
            
        return super().update(instance, validated_data)


# --- SÉRIALISEUR PLAT (GÉRÉ PAR L'ADMIN) ---

class PlatSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour la gestion (CRUD) des plats.
    """
    # NOTE : Le champ auteur_email est retiré car le champ 'auteur' n'est pas 
    # défini dans le modèle Plat. Si vous l'ajoutez à models.py, réintégrez cette ligne.
    # auteur_email = serializers.ReadOnlyField(source='auteur.email')

    class Meta:
        model = Plat
        fields = ['id', 'nom', 'description', 'prix_base', 'categorie', 'image', 'statut', 'variations']
        # Si vous ajoutez le champ 'auteur' au modèle Plat, ajoutez 'auteur' à read_only_fields ici.