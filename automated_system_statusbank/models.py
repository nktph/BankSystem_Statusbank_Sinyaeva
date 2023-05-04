from django.contrib.auth.models import User
from django.db import models

# Модели - аналог таблиц в базе данных. Здесь мы описываем поля и связи между объектами
# По здешним типам данных не вижу смысла давать пояснения - если англ хоть чуток понимаешь, то разберёшься что это


class Country(models.Model):
    # Параметры полей здесь: 1 - Человеческое название которое будет отображено в браузере
    # primary_key - поле является первичным ключом если True
    # unique - поле является уникальным если True
    # max_length - максимальная длина вводимых данных
    iso3code = models.CharField('Код страны', primary_key=True, unique=True, max_length=3)
    country_name = models.CharField('Название страны', unique=True, max_length=255)

    def __str__(self):
        # метод, который определяет что будет печататься, если мы не ссылаемся на кокретное поле класса,
        # т.е. обращаемся к самой модели, ниже будет пример. В данном случае мы будем печатать название страны
        return f'{self.country_name}'

    class Meta:
        # Этот служебный класс нужен для панели админа и ForeignKey-полей в моделях, которые от этой будут что-то
        # наследовать. Нужно это, чтобы модели отображались не на английском.
        # Поля в нём - названия модели в единственном и множественном числе
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'


class Address(models.Model):
    # Вот про что я говорил в методе __str__. В строке ниже мы не определяем имя поля Страны, поэтому в браузере
    # недостающие данные, такие как имя поля и варианты выбора, будут подтягиваться из класса Мета и метода __str__
    # Касаемо ForeignKey - в бд это аналог связи многие-к-одному. Первый параметр это модель, с которой мы хотим
    # связать данную. Параметр on_delete определяет, что делать если элемент
    # таблицы на которую мы ссылаемся будет удалён. В нашем случае CASCADE, это значит что при удалении из бд страны
    # все адреса которые ссылаются на эту страну будут удалены (что в принципе логично: нет страны - нет адресов в ней)
    country_iso3code = models.ForeignKey(Country, on_delete=models.CASCADE)
    city = models.CharField('Город', max_length=255)
    street_name = models.CharField('Улица', max_length=255)
    building_number = models.PositiveSmallIntegerField('Номер дома')
    apartment_number = models.PositiveSmallIntegerField('Номер квартиры')
    post_code = models.CharField('Почтовый индекс', max_length=255)

    def __str__(self):
        return f'{self.city} - {self.street_name} {self.building_number}-{self.apartment_number}'

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'


class Registration(models.Model):
    date_of_registration = models.DateField('Дата регистрации')
    registration_authority = models.CharField('Орган выдачи прописки', max_length=255)
    address = models.ForeignKey(Address, models.CASCADE)

    def __str__(self):
        return f'{self.address}'

    class Meta:
        verbose_name = 'Прописка'
        verbose_name_plural = 'Прописки'


SEX_CHOICES = [
    ('Мужской', 'Мужской'),
    ('Женский', 'Женский'),
]


class Passport(models.Model):
    first_name = models.CharField('Имя', max_length=255)
    last_name = models.CharField('Фамилия', max_length=255)
    patronymic = models.CharField('Отчество', max_length=255)
    birth_date = models.DateField('Дата рождения')
    series = models.CharField('Серия паспорта', max_length=255)
    number = models.PositiveIntegerField('Номер паспорта', unique=True)
    date_of_issue = models.DateField('Дата выдачи')
    date_of_expire = models.DateField('Действителен до')
    authority = models.CharField('Орган выдачи паспорта', max_length=255)

    # Тут пояснение насчёт параметра choices. Полов у нас лишь два, а поэтому нет смысла создавать для них отдельную
    # таблицу в бд. Над классом паспорта мы определили SEX_CHOICES - это что-то типо выбора из возможных вариантов,
    # т.е. пол человека не нужно (да и с таким подходом просто нельзя) писать ручками каждый раз
    # Параметр default нужен для затем, чтобы бд знала, что ей записывать в это поле если какием-то чудом пол указан не
    # будет (в данном случае благодаря SEX_CHOICES такое просто невозможно, но компилятор ругается если не указать)
    sex = models.CharField('Пол', choices=SEX_CHOICES, max_length=10, default='Неизвестно')

    # Параметр blank даёт возможность не указывать в поле в браузере ничего, null позволяет такое же, только для бд
    is_married = models.BooleanField('В браке', blank=True, null=True, default=False)
    country_iso3code = models.ForeignKey(Country, on_delete=models.CASCADE)
    registration = models.ForeignKey(Registration, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.patronymic}'

    class Meta:
        verbose_name = 'Паспорт'
        verbose_name_plural = 'Паспорта'


class Currency(models.Model):
    name = models.CharField('Наименование валюты', unique=True, max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Валюта'
        verbose_name_plural = 'Валюты'


class Client(models.Model):
    address_of_living = models.ForeignKey(Address, on_delete=models.CASCADE)
    company_name = models.CharField('Компания', max_length=255)
    position = models.CharField('Должность', max_length=255)
    income_per_month = models.PositiveIntegerField('Ежемесячный доход')
    email = models.EmailField('Email', unique=True)
    mobile_phone_number = models.CharField('Мобильный номер телефона', max_length=14, unique=True)
    home_phone_number = models.CharField('Домашний номер телефона', max_length=14)
    is_bound_to_military_service = models.BooleanField('Годен к воинской службе', blank=True, null=True, default=False)
    is_disabled = models.BooleanField('Инвалид', blank=True, null=True, default=False)
    is_retiree = models.BooleanField('Пенсионер', blank=True, null=True, default=False)
    passport = models.ForeignKey(Passport, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.passport}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


DEPOSIT_TYPES = [
    ('Безотзывной', 'Безотзывной'),
    ('Отзывной', 'Отзывной')
]


class DepositType(models.Model):
    type = models.CharField('Тип вклада', choices=DEPOSIT_TYPES, max_length=255, default='-')
    name = models.CharField('Название', max_length=255, default='-')
    description = models.CharField('Описание', max_length=500, default='-')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Тип депозита'
        verbose_name_plural = 'Типы депозитов'


class Deposit(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    contract_number = models.PositiveIntegerField('Номер договора', unique=True, default=1)
    deposit_type = models.ForeignKey(DepositType, on_delete=models.CASCADE)
    deposit_sum = models.DecimalField('Сумма депозита', max_digits=19, decimal_places=2)
    # on_delete=models.DO_NOTHING не удалит депозит из бд при удалении валюты
    currency = models.ForeignKey(Currency, on_delete=models.DO_NOTHING)
    date_of_issue = models.DateField('Дата заключения договора')
    date_of_expire = models.DateField('Дата окончания срока действия')
    percentage = models.FloatField('Проценты')
    worker = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    is_active = models.BooleanField('Активен', default=True)

    def __str__(self):
        return f'{self.client} - {self.deposit_type} - {self.deposit_sum}{self.currency}'

    class Meta:
        verbose_name = 'Депозит'
        verbose_name_plural = 'Депозиты'
