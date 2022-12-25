from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, views
from rest_framework.response import Response

from .models import Card
from .serializers import CardSerializer, GenerateCardSerializer, PaymentSerializer
from .services import generate_cards, make_payment


class GenerateCardView(views.APIView):
    def post(self, request):
        """Генерация карт"""
        generate_cards_data = GenerateCardSerializer(data=request.data)
        if generate_cards_data.is_valid():
            generate_cards(generate_cards_data.validated_data)
            return Response({'message': 'cards was created'})
        return Response({'message': 'not valid data'})


class CardList(generics.ListAPIView):
    """Отображение списка карт с возможностью фильтрации по полям"""
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['serial', 'number', 'created_at', 'end_of_serving_datetime', 'status']


class CardDetailView(views.APIView):
    def get(self, request, card_id: int):
        """Отображение деталей по карте со списком совершенных покупок"""
        card = Card.objects.prefetch_related('payment_set').get(pk=card_id)
        result = {'card_id': card.id, 'serial': card.serial, 'created_at': card.created_at,
                  'end_of_serving_datetime': card.end_of_serving_datetime, 'balance': card.balance,
                  'status': card.status, 'payments': []}
        payments = card.payment_set.all()
        for card_payment in payments:
            result['payments'].append({
                'payment_id': card_payment.id,
                'date_of_use': card_payment.date_of_use,
                'sum': card_payment.amount
            })
        return Response(data=result)

    def delete(self, request, card_id: int):
        """Удаление карты"""
        card = Card.objects.get(pk=card_id)
        card.delete()

        return Response(data={'message': 'card was deleted'})

    def patch(self, request, card_id: int):
        """Изменение статуса карты"""
        card = Card.objects.get(pk=card_id)
        if card.status == 'Activated':
            card.status = 'Unactivated'
            card.save()
            return Response(data={'message': 'Card is inactive now'})
        elif card.status == 'Unactivated':
            card.status = 'Activated'
            card.save()
            return Response(data={'message': 'Card is activated'})
        else:
            return Response(data={'message': 'Card is overdued'})


class PaymentView(views.APIView):
    def post(self, request):
        """Совершение платежа по карте"""
        payment = PaymentSerializer(data=request.data)
        if payment.is_valid():
            make_payment(payment.validated_data)
            return Response({'message': 'Payment was passed'})
        return Response({'message': 'not valid data'})
