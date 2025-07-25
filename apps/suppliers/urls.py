from rest_framework_extensions.routers import ExtendedDefaultRouter

from apps.dealerships.views import PurchaseViewSet, DiscountViewSet
from apps.suppliers.views import SupplierViewSet

suppliers_router = ExtendedDefaultRouter()

routes = suppliers_router.register(
    r'suppliers',
    SupplierViewSet,
    basename='supplier'
)
routes.register(
    r'purchases',
    PurchaseViewSet,
    basename='purchase',
    parents_query_lookups=['supplier']
)
routes.register(
    r'discounts',
    DiscountViewSet,
    basename='discount',
    parents_query_lookups=['supplier']
)

urlpatterns = suppliers_router.urls
