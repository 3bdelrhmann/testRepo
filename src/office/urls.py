from django.urls import path
from . import views

app_name = 'office'

urlpatterns = [
    path('',views.office_home,name='office_home'),
    path('agenda/',views.agenda,name='agenda'),
    path('agenda/create/',views.create_agenda,name='create_agenda'),
    path('agenda/created/<int:agenda_id>/',views.created_agenda,name='created_agenda'),
    path('agenda/update/<int:agenda_id>/',views.update_agenda,name='update_agenda'),

    path('clients/',views.customer_index,name='clients'),
    path('clients/create/',views.create_client,name='create_client'),
    path('clients/update/<int:client_id>/',views.update_client,name='update_client'),
    path('clients/created/<int:client_id>/',views.created_customer,name='created_customer'),
    
    path('assistants/update/<uuid:assistant_id>/',views.update_assistant,name='update_assistant'),
    path('assistants/create/',views.create_assistant,name='create_assistant'),
    path('assistants/created/<uuid:assistant_id>/',views.created_assistant,name='created_assistant'),
    path('invoices/',views.invoices,name='invoices'),
    path('contracts/',views.contract_forms,name='contract_forms'),
    path('assistants/',views.manage_assistants,name='manage_assistants'),
    path('invoices/create/',views.create_invoice,name='create_invoice'),
    path('invoices/detail/<int:invoice_id>/',views.invoice_detail,name='invoice_detail'),
    path('invoices/update/<int:invoice_id>/',views.invoice_update,name='invoice_update'),
]