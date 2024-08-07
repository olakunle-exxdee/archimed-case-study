from rest_framework import serializers

from .models import Bill, CapitalCall, Investment, Investor


class InvestorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investor
        fields = ["id", "name", "email"]


class InvestmentSerializer(serializers.ModelSerializer):
    email = serializers.CharField(write_only=True)

    class Meta:
        model = Investment
        fields = ["id", "amount", "date", "fee_percentage", "email"]

    def create(self, validated_data):
        investor_identifier = validated_data.pop("email")
        try:
            if "@" in investor_identifier:
                investor = Investor.objects.get(email=investor_identifier)
            else:
                investor = Investor.objects.get(id=investor_identifier)
        except Investor.DoesNotExist:
            raise serializers.ValidationError("Investor not found")

        investment = Investment.objects.create(investor=investor, **validated_data)
        return investment

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["investor"] = InvestorSerializer(instance.investor).data
        return representation


class BillSerializer(serializers.ModelSerializer):
    investor = InvestorSerializer()

    class Meta:
        model = Bill
        fields = "__all__"


class CapitalCallSerializer(serializers.ModelSerializer):
    investor = InvestorSerializer()
    bills = BillSerializer(many=True, read_only=True)

    class Meta:
        model = CapitalCall
        fields = "__all__"
