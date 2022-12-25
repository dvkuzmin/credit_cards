from django.urls import path

from .views import CardList, GenerateCardView, PaymentView, CardDetailView

urlpatterns = [
    path('generate_cards/', GenerateCardView.as_view(), name='generate_cards'),
    path('cards/', CardList.as_view(), name='card_list'),
    path('payment/', PaymentView.as_view(), name='payment'),
    path('cards/<int:card_id>/', CardDetailView.as_view(), name='card_detail')
]
