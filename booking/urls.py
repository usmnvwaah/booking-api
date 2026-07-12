from rest_framework.routers import DefaultRouter
from .views import ResourceViewSet, BookingViewSet

router = DefaultRouter()
router.register('resources', ResourceViewSet)
router.register('bookings', BookingViewSet, basename='bookings')

urlpatterns = router.urls