import random
import datetime

from .date_add_service import add_months
from card_service.models import Card
from card_service.tasks import check_active_period_of_card

MONTHS_ADD = {'1 month': 1, '6 months': 6, '1 year': 12}


def generate_quad_number() -> str:
    """Генерация 4 чисел для дальнейшей генерации номера карты в формате XXXX XXXX XXXX XXXX"""
    result = ''
    for i in range(4):
        result += str(random.randint(0, 9))
    return result


def generate_card_number(serial: str) -> str:
    """Генерация номера карты, в котором первые 4 цифры - серия карты"""
    card_number = serial + ' '
    for i in range(3):
        card_number += generate_quad_number()
        card_number += ' '
    card_number. strip()
    return card_number


def generate_cards(data: dict):
    """Генерация карт по параметрам пользователя
    data: dict - словарь со значениями:
    number_of_cards - Количество генерируемых карт
    serial - серия карты, первые 4 цифры
    active_during - сколько карта будет активна (1 месяц, 6 месяцев, 1 год)"""
    for i in range(data['number_of_cards']):
        serial_number = data['serial']
        card_number = generate_card_number(serial_number)
        serve_month_range = data['active_during']
        today = datetime.datetime.now()
        end_date_of_serve = add_months(today, MONTHS_ADD[serve_month_range])
        card = Card.objects.create(serial=serial_number,
                            number=card_number,
                            created_at=datetime.datetime.now(),
                            end_of_serving_datetime=end_date_of_serve)
        check_active_period_of_card.delay(card.pk)
