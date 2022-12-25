from django.db.models import F

from card_service.models import Payment


def make_payment(payment_data: dict):
    card = payment_data['card']
    amount = payment_data['amount']
    if card.balance >= amount:
        Payment.objects.create(amount=amount, card=card)
        card.balance = F('balance') - amount
        card.save()
