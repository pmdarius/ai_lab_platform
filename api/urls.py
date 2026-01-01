from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, WalletViewSet, GPUSlotViewSet,
    BookingViewSet, MentorViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'wallet', WalletViewSet)
router.register(r'slots', GPUSlotViewSet)
router.register(r'bookings', BookingViewSet)
router.register(r'mentors', MentorViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
