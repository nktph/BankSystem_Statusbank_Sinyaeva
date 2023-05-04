from django.urls import path
from . import views

app_name = 'automatedsystemstatusbank'
urlpatterns = [
    path('home/', views.home, name='home'),

    path('clients/', views.clients, name='clients'),
    path('clients/<int:client_id>/', views.client_details, name='client_details'),

    path('clients/<int:address_id>/edit/address/', views.edit_address, name='edit_client_address'),
    path('clients/<int:client_id>/edit/passport/', views.edit_passport, name='edit_client_passport'),
    path('clients/<int:client_id>/edit/personal/', views.edit_personal, name='edit_client_personal'),
    path('clients/<int:client_id>/delete/', views.delete_client, name='delete_client'),

    path('clients/add/', views.addclient, name='add_client'),

    path('deposits/', views.deposits, name='deposits'),
    path('deposits/<int:deposit_id>/', views.deposit_details, name='deposit_details'),
    path('deposits/<int:deposit_id>/edit/', views.edit_deposit, name='edit_deposit'),
    path('deposits/add', views.add_deposit, name='add_deposit'),
    path('deposits/<int:deposit_id>/delete/', views.delete_deposit, name='delete_deposit'),

]