from django.urls import path
from . import views

app_name = "office"

urlpatterns = [
    path('clients/search/',views.customer_index_search,name='customer_index_search'),
    path('clients/delete/',views.delete_from_customer_index,name='delete_from_customer_index'),
    path('clients/create/',views.create_new_client,name='create_new_client'),
    path('assistant/search/',views.search_assistant,name='search_assistant'),
    path('assistant/create/',views.create_assistant,name='create_assistant'),
    path('assistant/delete/',views.delete_assistant,name='delete_assistant'),
    path('invoices/search/',views.invoice_search,name='invoice_search'),
    path('invoices/delete/',views.delete_invoice,name='invoice_delete'),

    path('agenda/search/',views.agenda_search,name='agenda_search'),
    path('agenda/delete/',views.delete_agenda,name='agenda_delete'),
    path('contracts/search/',views.search_contracts,name='search_contracts'),
    
]