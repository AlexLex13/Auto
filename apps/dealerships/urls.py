from rest_framework_extensions.routers import ExtendedDefaultRouter

from apps.dealerships import views

dealerships_router = ExtendedDefaultRouter()

routes = dealerships_router.register(
    r'dealerships',
    views.DealershipViewSet,
    basename='dealership'
)
routes.register(
    r'preferences',
    views.DealershipPreferenceViewSet,
    basename='preference',
    parents_query_lookups=['dealership']
)
routes.register(
    r'cars',
    views.DealershipCarsViewSet,
    basename='dealership-cars',
    parents_query_lookups=['dealership']
)
routes.register(
    r'purchases',
    views.PurchaseViewSet,
    basename='purchase',
    parents_query_lookups=['dealership']
)

urlpatterns = dealerships_router.urls
