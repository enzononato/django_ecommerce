"""
URL configuration for django_ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include
from .views import home_page, about_page, contact_page
from accounts.views import register,login_view

urlpatterns = [
        path('', home_page, name='home'),
        path('about/', about_page),
	    path('contact/', contact_page),
        path('admin/', admin.site.urls),
        path('register/', register, name='register'),
        path('login/', login_view, name='login'),
        path('', include('django.contrib.auth.urls')),  # Inclui URLs de autenticação padrão do Django
        path('products/', include('products.urls')), # Inclui urls do app products
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)