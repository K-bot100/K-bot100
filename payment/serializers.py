from rest_framework import serializers
from .models import Payments
class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = ['date', 'transactionId','name', 'phoneNumber', 'community', 'productType', 'numberOfBuckets', 'amountPaid', 'status']