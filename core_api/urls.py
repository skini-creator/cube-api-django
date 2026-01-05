from django.urls import path
from .views import (
    RegisterView,
    PlatListCreateView,
    PlatRetrieveUpdateDestroyView
)

urlpatterns = [
    # AUTHENTIFICATION
    path('auth/register/', RegisterView.as_view(), name='auth_register'),
    
    # PLATS
    path('plats/', PlatListCreateView.as_view(), name='plat_list_create'),
    path('plats/<int:pk>/', PlatRetrieveUpdateDestroyView.as_view(), name='plat_retrieve_update_destroy'),
]