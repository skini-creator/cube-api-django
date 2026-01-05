# core_api/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

# --- 0. RBAC (Permissions et Rôles) ---
# Nécessaire pour les sections 6 et 7 de la spec
class Permission(models.Model):
    key = models.CharField(max_length=50, unique=True, help_text="Ex: orders.preparation.update")
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.key

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    permissions = models.ManyToManyField(Permission, blank=True)

    def __str__(self):
        return self.name
    
# --- 1. Modèle Utilisateur Personnalisé (CLIENT) ---
class Client(AbstractUser):
    # Champ spécifique requis par la spec (AUTH/login)
    telephone = models.CharField(max_length=15, unique=True)
    
    # Redéfinition du champ email comme unique (bonne pratique)
    email = models.EmailField(unique=True, blank=True, null=True)
    
    # Utilisation du téléphone pour la connexion (selon la spec)
    USERNAME_FIELD = 'telephone'
    # Champs requis lors de la création d'un utilisateur
    REQUIRED_FIELDS = ['email', 'username'] 
    
    # Assurer que 'nom_complet' est pris en compte, utiliser le champ 'first_name' pour cela
    # Si le frontend envoie 'nom_complet', il faudra le mapper à 'first_name' ou le stocker ici:
    nom_complet = models.CharField(max_length=255) # Ajout du champ explicite pour le FEO

    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True) # Pour les admins

    def get_permissions_list(self):
        # Pour répondre au contrat FEO dans /auth/profile
        if self.role:
            return list(self.role.permissions.values_list('key', flat=True))
        return []

    def __str__(self):
        return self.telephone

# --- 2. Modèle Administrateur (ADMIN) ---
# Note: Dans un projet professionnel, Admin hériterait souvent d'AbstractUser aussi, 
# mais ici nous pouvons simplifier en le liant au Client/Utilisateur si nécessaire.
# Pour l'instant, gardons-le simple comme un profil lié.
class Admin(models.Model):
    user = models.OneToOneField(Client, on_delete=models.CASCADE) # Lier à l'utilisateur
    # Note: le rôle est déjà dans Client pour l'RBAC.
    
    def __str__(self):
        return f"Admin: {self.user.nom_complet}"

# --- 3. Modèle Plat ---
class Plat(models.Model):
    TYPE_CHOICES = [
        ('MENU', 'Menu'),
        ('BASE', 'Base'),
        ('ACCOMPAGNEMENT', 'Accompagnement'),
        ('SUPPLEMENT', 'Supplément'),
    ]
    STATUT_CHOICES = [
        ('ACTIF', 'Actif'),
        ('INACTIF', 'Inactif'),
        ('EPUISE', 'Épuisé'),
    ]
    
    nom = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='BASE')
    prix_base = models.DecimalField(max_digits=6, decimal_places=2) 
    categorie = models.CharField(max_length=100) # Pour le filtre /plats/categories
    image = models.URLField(blank=True, null=True) # URL renvoyée par /plats/upload
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='ACTIF')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Variations du plat (Champ JSON ou ManyToMany si complexe)
    # Pour simplifier, utilisons JSONField pour stocker des structures (ex: taille/options)
    variations = models.JSONField(default=list, blank=True) 

    def __str__(self):
        return self.nom

# --- 4. Modèles Panier (Cart) ---
class Panier(models.Model):
    client = models.OneToOneField(Client, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    # Champ pour gérer la promotion appliquée (POST /panier/promo)
    code_promo = models.CharField(max_length=50, blank=True, null=True)
    reduction = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    
    def __str__(self):
        return f"Panier de {self.client.telephone}"

class LignePanier(models.Model):
    panier = models.ForeignKey(Panier, on_delete=models.CASCADE, related_name='items')
    plat = models.ForeignKey(Plat, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=1)
    # Pour stocker la variation choisie (id_variation?)
    id_variation = models.CharField(max_length=50, blank=True, null=True)
    # Pour stocker la personnalisation (ex: sans oignon)
    personnalisation = models.TextField(blank=True, null=True)

# --- 5. Modèles Commande (Orders) ---
class Commande(models.Model):
    STATUT_CHOICES = [
        ('EN_ATTENTE', 'En attente'),
        ('CONFIRMEE', 'Confirmée'),
        ('EN_PREPARATION', 'En préparation'),
        ('EN_LIVRAISON', 'En livraison'),
        ('LIVREE', 'Livrée'),
        ('ANNULEE', 'Annulée'),
    ]
    
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name='commandes')
    
    # Informations de livraison (selon CommandeRequest)
    adresse_livraison = models.CharField(max_length=255)
    ville = models.CharField(max_length=100)
    commune = models.CharField(max_length=100)
    instructions = models.TextField(blank=True, null=True)
    
    # Statuts et dates
    statut_commande = models.CharField(max_length=20, choices=STATUT_CHOICES, default='EN_ATTENTE')
    date_commande = models.DateTimeField(auto_now_add=True)
    date_confirmation = models.DateTimeField(null=True, blank=True)
    date_preparation = models.DateTimeField(null=True, blank=True)
    date_depart_livraison = models.DateTimeField(null=True, blank=True)
    date_livree = models.DateTimeField(null=True, blank=True)

    # Récapitulatif financier
    sous_total = models.DecimalField(max_digits=8, decimal_places=2)
    frais_livraison = models.DecimalField(max_digits=8, decimal_places=2)
    tva = models.DecimalField(max_digits=8, decimal_places=2)
    total = models.DecimalField(max_digits=8, decimal_places=2)

    # Suivi du livreur
    # Champs pour /commandes/:id/track
    livreur_position_lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    livreur_position_lng = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return f"Commande #{self.id} - {self.statut_commande}"

class LigneCommande(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE, related_name='lignes')
    plat = models.ForeignKey(Plat, on_delete=models.PROTECT) # On ne supprime pas le plat si une commande existe
    quantite = models.PositiveIntegerField()
    prix_unitaire = models.DecimalField(max_digits=8, decimal_places=2) # Prix figé à la commande
    id_variation = models.CharField(max_length=50, blank=True, null=True)
    personnalisation = models.TextField(blank=True, null=True)

# --- 6. Modèle Paiement ---
class Paiement(models.Model):
    MODE_CHOICES = [
        ('AIRTEL_MONEY', 'Airtel Money'),
        ('MOBILE_CASH', 'Mobile Cash'),
        ('LIVRAISON', 'Paiement à la livraison'),
    ]
    STATUT_CHOICES = [
        ('EN_ATTENTE', 'En attente'),
        ('CONFIRME', 'Confirmé'),
        ('ECHEC', 'Échec'),
    ]
    
    commande = models.OneToOneField(Commande, on_delete=models.CASCADE, related_name='paiement')
    mode = models.CharField(max_length=20, choices=MODE_CHOICES)
    montant = models.DecimalField(max_digits=8, decimal_places=2)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='EN_ATTENTE')
    
    # Pour les paiements électroniques
    reference = models.CharField(max_length=100, blank=True, null=True)
    date_paiement = models.DateTimeField(null=True, blank=True)
    redirect_url = models.URLField(max_length=500, null=True, blank=True) # Pour les redirections après paiement
    
    # Champ spécifique pour la livraison (montant_en_especes)
    montant_en_especes = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True) # Requis par la spec /commandes

    def __str__(self):
        return f"Paiement #{self.id} - {self.get_statut_display()}"

# --- 7. Modèles Utilitaires (Paramètres et Communes) ---
class ParametresRestaurant(models.Model):
    # GET /parametres, PATCH /parametres
    nom_restaurant = models.CharField(max_length=100, default="Le Cube")
    adresse = models.CharField(max_length=255, blank=True, null=True)
    paiement_airtel_active = models.BooleanField(default=True)
    paiement_mobilecash_active = models.BooleanField(default=True)
    paiement_livraison_active = models.BooleanField(default=True)
    taux_tva = models.DecimalField(max_digits=4, decimal_places=2, default=0.18) # 18%
    
    class Meta:
        verbose_name_plural = "Paramètres du Restaurant"
        # Assurer qu'il n'y a qu'une seule instance de paramètres
        default_permissions = () 

class Commune(models.Model):
    # GET /communes
    nom = models.CharField(max_length=100, unique=True)
    frais_livraison = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.nom