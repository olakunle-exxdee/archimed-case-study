from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import BillViewSet, CapitalCallViewSet, InvestmentViewSet, InvestorViewSet

router = DefaultRouter()
router.register(r"investors", InvestorViewSet)
router.register(r"investments", InvestmentViewSet)
router.register(r"bills", BillViewSet)
router.register(r"capital-calls", CapitalCallViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
