from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import *


def index(request):  # Приветственная страница
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('automatedsystemstatusbank:home'))
    else:
        return render(request, "index.html")


def home(request):  # Главная страница
    if not request.user.is_authenticated:  # Эта штука есть в начале каждой функции: если пользователь не авторизован,
        # его перебросит на приветственную страницу, которая попросит авторизоваться
        return HttpResponseRedirect(reverse(index))
    else:
        return render(request, "home.html")


def clients(request):  # Список клиентов
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse(index))
    client_list = Client.objects.order_by('passport__last_name')  # Получаем из бд список клиентов, упорядоченный по фамилии
    return render(request, "clients/clients.html", {'clients': client_list})
    # ^ тут мы возвращаем html-страницу с помещёнными в неё данными.
    # Данные кидаем по принципу: {'как_обращаемся_в_html-шаблоне': переменная_из_которой_берём_данные}


def addclient(request):  # Добавление нового клиента
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse(index))
    if request.method == "POST":  # Сюда алгоритм зайдёт когда пользователь заполнит форму и нажмёт "сохранить"
        address_formset = AddressFormSet(request.POST)
        if address_formset.is_valid():  # Проверка корректности данных в форме
            for form in address_formset:
                form.save()  # На основе формы создаётся модель и сохраняется в бд

        registration_form = RegistrationForm(request.POST)
        if registration_form.is_valid():
            registration = registration_form.save(commit=False)  # Модель создастся, но в бд не зальётся. Это мы делаем,
            # чтобы в следующей строчке добавить поле адреса, которое мы не выводили для формы
            registration.address = Address.objects.last()  # Достаём из бд последний созданный адрес (по логике работы
            # именно он нам и нужен)
            registration.save()

        passport_form = PassportForm(request.POST)
        if passport_form.is_valid():
            passport = passport_form.save(commit=False)
            passport.registration = Registration.objects.last()
            passport.save()

        client_form = ClientForm(request.POST)
        if client_form.is_valid():
            client = client_form.save(commit=False)
            client.address_of_living = Address.objects.get(id=registration.address.id - 1)  # Тут мы достаём
            # предпоследний адрес, так как в форме клиента мы заполняли два адреса, и сохраняются они в таком порядке:
            # сначала сохранятся адрес проживания, потом адрес прописки. В бд они так и будут расположены: предпоследний
            # и последний
            client.passport = Passport.objects.last()
            client.save()
            return HttpResponseRedirect(reverse('automatedsystemstatusbank:client_details', args=(client.id,)))
            # ^ перенаправляем на страницу полной информации созданного клиента
    else:
        # Сюда мы попадаем при первом открытии страницы - т.е. до заполнения данных формы
        address_formset = AddressFormSet(queryset=Address.objects.filter(city__startswith='0'))
        registration_form = RegistrationForm()
        passport_form = PassportForm()
        client_form = ClientForm()
        return render(request, "clients/client_new.html", {'address_formset': address_formset,
                                                           'registration_form': registration_form,
                                                           'passport_form': passport_form,
                                                           'client_form': client_form})


def edit_address(request, address_id):  # Редактирование адреса клиента
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse(index))
    address = get_object_or_404(Address, id=address_id)  # Получаем из бд адрес, ищем по id. Если не найдёт - выбросит
                                                        # страницу 404
    if request.method == "POST":
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            client = Client.objects.get(address_of_living=address)
            return HttpResponseRedirect(reverse('automatedsystemstatusbank:client_details', args=(client.id,)))
    else:
        form = AddressForm(instance=address)  # При открытии страницы форма будет уже предзаполнена, т.к. мы хотим
        # отредактировать уже существующую, а не создать новую
        return render(request, 'clients/client_edit.html', {'form': form,
                                                            'title': 'Адрес'})


def edit_passport(request, client_id):  # Редактирование паспортных данных клиента
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse(index))
    client = get_object_or_404(Client, id=client_id)
    if request.method == "POST":
        form = PassportForm(request.POST, instance=client.passport)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('automatedsystemstatusbank:client_details', args=(client.id,)))
    else:
        form = PassportForm(instance=client.passport)
        return render(request, 'clients/client_edit.html', {'form': form,
                                                            'title': 'Паспортные данные'})


def edit_personal(request, client_id):  # Редактирование персональной информации клиента
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse(index))
    client = get_object_or_404(Client, id=client_id)
    if request.method == "POST":
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('automatedsystemstatusbank:client_details', args=(client.id,)))
    else:
        form = ClientForm(instance=client)
        return render(request, 'clients/client_edit.html', {'form': form,
                                                            'title': 'Персональные данные'})


def client_details(request, client_id):  # Полная информация клиента
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse(index))

    client = get_object_or_404(Client, id=client_id)
    return render(request, "clients/client_detail.html", {'client': client})


def delete_client(request, client_id):  # Удаление клиента
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse(index))
    client = get_object_or_404(Client, id=client_id)  # Достаём из бд нужного клиента
    client.delete()  # Удаляем клиента из бд
    return HttpResponseRedirect(reverse('automatedsystemstatusbank:clients'))
    # ^ Перенаправляем на список клиентов


def deposits(request):  # Список депозитов
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse(index))
    deposit_list = Deposit.objects.all()
    return render(request, "deposits/deposits.html", {'deposits': deposit_list})


def deposit_details(request, deposit_id):  # Полная информация о депозите
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse(index))
    deposit = get_object_or_404(Deposit, id=deposit_id)

    return render(request, "deposits/deposit_details.html", {'deposit': deposit})


def add_deposit(request):  # Добавление депозита
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse(index))

    if request.method == "POST":
        form = DepositForm(request.POST)
        if form.is_valid():
            deposit = form.save(commit=False)  # Создаём модель, но не сохраняем в бд
            deposit.worker = User.objects.get(username=request.user.username)  # Поле работника заполнится автоматически
            # из данных авторизованного пользователя
            deposit.save()

            return HttpResponseRedirect(reverse('automatedsystemstatusbank:deposit_details', args=(deposit.id,)))
    else:
        form = DepositForm()
    return render(request, "deposits/deposit_new.html", {'form': form})


def edit_deposit(request, deposit_id):  # Редактирование депозитов
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse(index))
    deposit = get_object_or_404(Deposit, id=deposit_id)
    if request.method == "POST":
        form = DepositForm(request.POST, instance=deposit)
        if form.is_valid():
            deposit = form.save()
            return HttpResponseRedirect(reverse('automatedsystemstatusbank:deposit_details', args=(deposit.id,)))
    else:
        form = DepositForm(instance=deposit)
    return render(request, 'deposits/deposit_new.html', {'form': form, 'edit': True})


def delete_deposit(request, deposit_id):  # Удаление депозита
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse(index))
    deposit = get_object_or_404(Deposit, id=deposit_id)
    deposit.delete()
    return HttpResponseRedirect(reverse('automatedsystemstatusbank:deposits'))
