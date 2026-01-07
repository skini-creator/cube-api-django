# core_api/admin.py

from django.contrib import admin
from .models import (
    CustomUser, Role, Permission, Plat, Commande, 
    LigneCommande, Panier, LignePanier, Commune, 
    ParametresRestaurant, Paiement
)

# Configuration de l'affichage pour l'utilisateur personnalisé
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('telephone', 'email', 'nom_complet', 'is_staff', 'is_active', 'role')
    search_fields = ('telephone', 'email', 'nom_complet')
    list_filter = ('is_staff', 'is_active', 'role')

# Configuration pour les Rôles et Permissions (RBAC)
class RoleAdmin(admin.ModelAdmin):
    # Correction: 'description' est souvent un champ non existant, nous le supprimons
    # Si votre modèle Role a un champ 'description', vous pouvez le remettre.
    list_display = ('name',) # Seul le nom est affiché

class PermissionAdmin(admin.ModelAdmin):
    list_display = ('key', 'description')

# Configuration pour les Plats
class PlatAdmin(admin.ModelAdmin):
    list_display = ('nom', 'type', 'categorie', 'prix_base', 'statut')
    list_filter = ('type', 'categorie', 'statut')
    search_fields = ('nom', 'description')
    
# Configuration pour la Commande
class LigneCommandeInline(admin.TabularInline):
    model = LigneCommande
    extra = 0

class CommandeAdmin(admin.ModelAdmin):
    # Correction 1: Changement de 'id_client' à 'client'
    list_display = ('id', 'client', 'statut_commande', 'total', 'date_commande')
    
    # Correction 2: Suppression du filtre 'mode_paiement' (champ non trouvé)
    list_filter = ('statut_commande', 'date_commande') 
    
    # Correction 1: Changement de 'id_client__...' à 'client__...'
    search_fields = ('id', 'client__telephone', 'client__nom_complet')
    inlines = [LigneCommandeInline]

# Configuration pour les autres modèles
class CommuneAdmin(admin.ModelAdmin):
    list_display = ('nom', 'frais_livraison')

# Enregistrement de tous les modèles
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Permission, PermissionAdmin)

admin.site.register(Plat, PlatAdmin)
admin.site.register(Commande, CommandeAdmin)

admin.site.register(Commune, CommuneAdmin)
admin.site.register(ParametresRestaurant) 
admin.site.register(Paiement)
admin.site.register(Panier)
admin.site.register(LignePanier)