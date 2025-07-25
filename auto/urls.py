"""
URL configuration for auto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import include, path
from debug_toolbar.toolbar import debug_toolbar_urls
from django.views.generic import RedirectView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from apps.cars.urls import cars_router
from apps.dealerships.urls import dealerships_router
from apps.suppliers.urls import suppliers_router
from apps.customers.urls import customers_router

schema_view = get_schema_view(
   openapi.Info(
      title="Auto API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny,],
)

swagger_urls = [
    path('swagger.<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]


router = DefaultRouter()
router.registry.extend(cars_router.registry)
router.registry.extend(dealerships_router.registry)
router.registry.extend(suppliers_router.registry)
router.registry.extend(customers_router.registry)


urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('', RedirectView.as_view(url='api/v1/')),
    path('admin/', admin.site.urls),
    path('accounts/', include('apps.user_auth.urls')),
] + swagger_urls + debug_toolbar_urls()
