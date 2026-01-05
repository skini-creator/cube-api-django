from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Plat, Role # Assurez-vous que Role est bien importé

User = get_user_model()

# --- SÉRIALISEUR UTILISATEUR (AUTHENTIFICATION) ---

class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'role', 'is_active', 'is_staff']
        extra_kwargs = {'password': {'write_only': True}} 

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        
        # Le rôle par défaut est 'CLIENT'
        validated_data['role'] = Role.CLIENT 
        
        instance = self.Meta.model(**validated_data)
        
        if password is not None:
            instance.set_password(password)
        
        instance.save()
        return instance

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password is not None:
            instance.set_password(password)
            
        return super().update(instance, validated_data)


# --- SÉRIALISEUR PLAT (GÉRÉ PAR L'ADMIN) ---

class PlatSerializer(serializers.ModelSerializer):
    auteur_email = serializers.ReadOnlyField(source='auteur.email')

    class Meta:
        model = Plat
        fields = ['id', 'nom', 'description', 'prix', 'disponible', 'auteur', 'auteur_email', 'date_creation']
        read_only_fields = ['auteur']