from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Bill, CapitalCall, Investment, Investor
from .serializers import (
    BillSerializer,
    CapitalCallSerializer,
    InvestmentSerializer,
    InvestorSerializer,
)
from .utils import generate_bills, generate_capital_call


class InvestorViewSet(viewsets.ModelViewSet):
    queryset = Investor.objects.all()
    serializer_class = InvestorSerializer


class InvestmentViewSet(viewsets.ModelViewSet):
    queryset = Investment.objects.all()
    serializer_class = InvestmentSerializer


class BillViewSet(viewsets.ModelViewSet):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer

    @action(detail=False, methods=["post"])
    def generate(self, request):
        investor_id = request.data.get("investor_id")
        if not investor_id:
            return Response({"error": "Investor ID is required"}, status=400)

        bills = generate_bills(investor_id)
        serializer = self.get_serializer(bills, many=True)
        return Response(serializer.data)


class CapitalCallViewSet(viewsets.ModelViewSet):
    queryset = CapitalCall.objects.all()
    serializer_class = CapitalCallSerializer

    @action(detail=False, methods=["post"])
    def generate(self, request):
        investor_id = request.data.get("investor_id")
        if not investor_id:
            return Response({"error": "Investor ID is required"}, status=400)

        capital_call = generate_capital_call(investor_id)
        serializer = self.get_serializer(capital_call)
        return Response(serializer.data)
