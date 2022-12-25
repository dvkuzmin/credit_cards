from django.db import models

STATUS_CHOICES = [
    ('Activated', 'Активирована'),
    ('Unactivated', 'Не активирована'),
    ('Overdued', 'Просрочена')
]


class Card(models.Model):
    serial = models.CharField('Серия карты', max_length=20)
    number = models.CharField('Номер карты', max_length=20)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    end_of_serving_datetime = models.DateTimeField('Дата окончания обслуживания')
    balance = models.IntegerField('Баланс', default=1000)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='Activated')

    def __str__(self):
        return f'credit card with number {self.number}'


class Payment(models.Model):
    date_of_use = models.DateTimeField('Дата совершения платежа', auto_now_add=True)
    amount = models.IntegerField('Сумма платежа')
    card = models.ForeignKey('Card', on_delete=models.CASCADE)
