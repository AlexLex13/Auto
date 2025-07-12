from rest_framework.routers import DefaultRouter

from apps.cars import views

cars_router = DefaultRouter()
cars_router.register(r'cars', views.CarViewSet, basename='car')

urlpatterns = cars_router.urls
