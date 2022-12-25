from rest_framework import serializers

from .models import Card, Payment

DATE_CHOICES = [
    ('1 year', '1 год'),
    ('6 months', '6 месяцев'),
    ('1 month', '1 месяц'),
]


class GenerateCardSerializer(serializers.Serializer):
    serial = serializers.CharField(max_length=4)
    number_of_cards = serializers.IntegerField()
    active_during = serializers.ChoiceField(choices=DATE_CHOICES)


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['pk', 'serial', 'number', 'created_at', 'end_of_serving_datetime', 'balance', 'status']


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['amount', 'card']
