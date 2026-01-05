from django.contrib import admin
from django.urls import path, include

# Importation des vues de JWT
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # AUTHENTIFICATION JWT : Login et Refresh
    path('api/v1/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # API Principale (Registration, Plats, etc.)
    path('api/v1/', include('core_api.urls')),
]