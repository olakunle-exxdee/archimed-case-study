from rest_framework import serializers

from .models import Bill, CapitalCall, Investment, Investor


class InvestorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investor
        fields = ["id", "name", "email"]


class InvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investment
        fields = "__all__"


class BillSerializer(serializers.ModelSerializer):
    investor = InvestorSerializer()

    class Meta:
        model = Bill
        fields = ["id", "bill_type", "amount", "date", "investor"]


class CapitalCallSerializer(serializers.ModelSerializer):
    investor = InvestorSerializer()
    bills = BillSerializer(many=True, read_only=True)

    class Meta:
        model = CapitalCall
        fields = ["id", "total_amount", "status", "bills", "investor"]
