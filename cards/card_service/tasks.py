import datetime
import time
import pytz

from cards.celery import app

from .models import Card


@app.task
def check_active_period_of_card(card_id: int):
    """Таска для проверки срока обслуживания карты"""
    while True:
        try:
            card = Card.objects.get(pk=card_id)
            if card.end_datetime < (datetime.datetime.now(tz=pytz.timezone('Europe/Moscow'))):
                card.status = 'Overdued'
                card.save()
                return
            time.sleep(300)
        except:
            return
