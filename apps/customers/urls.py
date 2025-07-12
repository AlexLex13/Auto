from rest_framework_extensions.routers import ExtendedDefaultRouter

from apps.customers.views import CustomerViewSet, OfferViewSet
from apps.dealerships.views import PurchaseViewSet

customers_router = ExtendedDefaultRouter()

routes = customers_router.register(
    r'customers',
    CustomerViewSet,
    basename='customer'
)
routes.register(
    r'purchases',
    PurchaseViewSet,
    basename='purchase',
    parents_query_lookups=['customer']
)
routes.register(
    r'offers',
    OfferViewSet,
    basename='offer',
    parents_query_lookups=['customer']
)

urlpatterns = customers_router.urls
