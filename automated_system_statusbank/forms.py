from django import forms
from django.forms import modelformset_factory
from .models import *

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = '__all__'
        labels = {
            'country_iso3code': 'Страна',
        }

AddressFormSet = modelformset_factory(Address, AddressForm, extra=2,)

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = '__all__'
        exclude = ('address',)
        labels = {
            'address': 'Адрес',
        }

class PassportForm(forms.ModelForm):
    class Meta:
        model = Passport
        fields = '__all__'
        exclude = ('registration',)
        labels = {
            'country_iso3code': 'Гражданство',
        }

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        exclude = ('passport', 'address_of_living')
        labels = {
            'country_iso3code': 'Страна',
        }

class DepositForm(forms.ModelForm):
    class Meta:
        model = Deposit
        exclude = ('worker',)
        labels = {
            'client': 'Клиент',
            'credit_type': 'Тип кредита',
            'currency': 'Валюта',
            'deposit_type': 'Тип вклада'
        }