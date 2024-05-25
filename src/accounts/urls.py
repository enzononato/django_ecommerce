from django.urls import path
from .views import register, login_view, logout

urlpatterns = [
    path('register/', register, name='register'), # Adiciona a URL de registro
    path('login/', login_view, name='login'), # Adiciona a URL de login
    path('logout/', logout, name='logout'),  # Adiciona a URL de logout
]
