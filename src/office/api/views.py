from .serializers import InvoiceSerializer,AgendaSerializer,CustomerIndexSerializer,ContractsSerializer,AsistantSerializer
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from accounts.decorators import twofa_required
from rest_framework.response import Response
from django.core.paginator import Paginator
from office.forms import CustomerIndexForm,AssistantForm
from django.http import JsonResponse
from rest_framework import status
from office.models import Invoice,ContractsForms,CustomerIndex
from django.core import serializers
from accounts.models import User
from django.db.models import Q


@twofa_required
@login_required()
@api_view(['GET'])
def invoice_search(request):

    current_user = request.user

    if reuest.user.is_assistant:
        current_user = request.user.assistant_to

    if request.method == 'GET' and request.is_ajax():
        query = request.GET.get('query')
        page  = request.GET.get('page_num')
        if query == False or not query:
            data  = current_user.all_invoices.all().order_by('-registered_at')
        elif query.isdigit():
            data  = current_user.all_invoices.filter(id=query)
        else:
            data  = data.filter(Q(customer_name__icontains=query) | Q(lawyer_name__icontains=query))
        if data.exists():
            pagination = Paginator(data,10)
            if int(page) > pagination.num_pages:
                data = {}
            else:
                data = pagination.get_page(page)
        serializer  = InvoiceSerializer(data,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    return Response({''},status=status.HTTP_401_UNAUTHORIZED)


@twofa_required
@login_required()
@api_view(['GET'])
def agenda_search(request):
    if request.method == 'GET' and request.is_ajax():
        pass
        if request.user.is_assistant:
            pass
        else:
            lawyer   = request.GET.get('lawyer')
            query    = request.GET.get('query')
            session_date     = request.GET.get('session_date')
            page     = request.GET.get('page_num')
            data  = request.user.lawyer_agenda.all().order_by('-created_at')
            if data:
                if lawyer:
                    data  = data.filter(assign_to=lawyer)
                if session_date:
                    data  = data.filter(session_date=session_date)
                if query:
                    query_result  = data.filter(case_id__icontains=query)
                    if not query_result:
                        query_result = data.filter(case_year__icontains=query)
                    if not query_result:
                        query_result = data.filter(court__icontains=query)
                    if not query_result:
                        query_result   = data.filter(customer_name__icontains=query)
                    if not query_result:
                        query_result   = data.filter(customer_mobile=query)
                    data = query_result
                if data:
                    pagination = Paginator(data,4)
                    if int(page) > pagination.num_pages:
                        data = {}
                    else:
                        data = pagination.get_page(page)
            serializer  = AgendaSerializer(data,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
    return Response({''},status=status.HTTP_401_UNAUTHORIZED)

@twofa_required
@login_required()
@api_view(['GET'])
def customer_index_search(request):
    if request.method == 'GET' and request.is_ajax():
        if request.user.is_assistant:
            pass
        else:
            lawyer   = request.GET.get('lawyer')
            query    = request.GET.get('query')
            page     = request.GET.get('page_num')
            data  = request.user.lawyer_customers.all().order_by('-created_at')
            if data:
                if lawyer:
                    data  = data.filter(assign_to=lawyer)
                if query:
                    query_result = data.filter(file_id=query)
                    if not query_result:
                        query_result   = data.filter(customer_name__icontains=query)
                    if not query_result:
                        query_result   = data.filter(customer_mobile=query)
                    data = query_result
                if data:
                    pagination = Paginator(data,4)
                    if int(page) > pagination.num_pages:
                        data = {}
                    else:
                        data = pagination.get_page(page)
            serializer  = CustomerIndexSerializer(data,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
    return Response({''},status=status.HTTP_401_UNAUTHORIZED)

@twofa_required
@login_required()
@api_view(['POST'])
def create_new_client(request):
    if request.method == 'POST' and request.is_ajax():
        if request.user.is_assistant:
            pass
        else:
            form = CustomerIndexForm(user=request.user,data=request.POST)
            if form.is_valid():
                print('-'*20)
                print(form.cleaned_data)
                add_lawyer        = form.save(commit=False)
                add_lawyer.lawyer = request.user
                data    = add_lawyer.save()
                # print(data)
                # nw_data = CustomerIndexSerializer(data)
                # # # serialzer = serializers.serialize('json',)
                # print('data' * 10)
                # print(nw_data.data) #01276138545

                return JsonResponse(data,status=status.HTTP_201_CREATED,safe=False)
            else:
                data = form.errors.as_json()
                return Response(data,status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    return Response({''},status=status.HTTP_401_UNAUTHORIZED)

@twofa_required
@login_required()
@api_view(['GET'])
def search_contracts(request):
    if request.method == 'GET' and request.is_ajax():
        query = request.GET.get('query')
        page  = request.GET.get('page_num')
        if query:
            data = ContractsForms.objects.filter(title__icontains=query)
        else:
            data = ContractsForms.objects.all()

        pagination = Paginator(data,1)
        if int(page) > pagination.num_pages:
            data = {}
        else:
            data = pagination.get_page(page)
        
        serialzer = ContractsSerializer(data,many=True)
        return Response(serialzer.data,status=status.HTTP_200_OK)
        
    return Response({''},status=status.HTTP_401_UNAUTHORIZED)

@twofa_required
@login_required()
@api_view(['GET'])
def search_assistant(request):
    if request.method == 'GET' and request.is_ajax():
        if request.user.is_assistant:
            pass
        else:
            data = request.user.lawyer_assistants.all().order_by('-register_date')
            query = request.GET.get('query')
            page  = int(request.GET.get('page_num'))
            if query:
                data  = data.filter(Q(first_name__icontains=query) | Q(email__icontains=query))
            pagination = Paginator(data,5)  
            if int(page) > pagination.num_pages:
                data = {}
            else:
                data = pagination.get_page(page)
            serializer = AsistantSerializer(data,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
    return Response({''},status=status.HTTP_401_UNAUTHORIZED)


@twofa_required
@login_required()
@api_view(['POST'])
def create_assistant(request):
    if request.user.is_assistant:
        pass
    else:
        if request.method == 'POST' and request.is_ajax():
            form = AssistantForm(request.POST)
            if form.is_valid():
                data = form.save(commit=False)
                data.is_assistant = True
                data.phone_number = None
                data.onsite_cost  = 0
                data.phone_cost   = 0
                data.send_code    = False
                data.assistant_to = request.user
                data.blocked_booking      = False
                data.allow_reset_password = False
                data.first_name = data.first_name + ' ' +data.last_name 
                data.last_name  = None
                data.save()
                serialzer = serializers.serialize('json',[data,])
                return Response(serialzer,status=status.HTTP_201_CREATED)
            else:
                data = form.errors.as_json()
                return Response(data,status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    return Response({''},status=status.HTTP_401_UNAUTHORIZED)


@twofa_required
@login_required()
@api_view(['DELETE'])
def delete_from_customer_index(request):
    if request.method == 'DELETE' and request.is_ajax():    
        customer_id = request.POST.get('delete_obj_id')
        print('**' * 50)
        print(customer_id)
        print('**' * 50)
        if request.user.is_assistant:
            pass
        else:
            try:
                get_customer = request.user.lawyer_customers.get(id=customer_id)
                get_customer.delete()
                return Response({'status':'success'},status=status.HTTP_200_OK)
            except:
                return Response({'status':'error'},status=status.HTTP_404_NOT_FOUND)
    return Response({''},status=status.HTTP_401_UNAUTHORIZED)


@twofa_required
@login_required()
@api_view(['DELETE'])
def delete_assistant(request):
    if request.method == 'DELETE' and request.is_ajax():
        assistant_id = request.POST.get('delete_obj_id')
        if request.user.is_assistant:
            pass
        else:
            try:
                get_customer = request.user.lawyer_assistants.get(id=assistant_id)
                get_customer.delete()
                return Response({'status':'success'},status=status.HTTP_200_OK)
            except:
                return Response({'status':'error'},status=status.HTTP_404_NOT_FOUND)
    return Response({''},status=status.HTTP_401_UNAUTHORIZED)

@twofa_required
@login_required()
@api_view(['DELETE'])
def delete_agenda(request):
    agenda_id = request.POST.get('delete_obj_id')
    if request.method == 'DELETE' and request.is_ajax():
        if request.user.is_assistant:
            pass
        else:
            try:
                get_agenda = request.user.lawyer_agenda.get(id=agenda_id)
                get_agenda.delete()
                return Response({'status':'success'},status=status.HTTP_200_OK)
            except:
                return Response({'status':'error'},status=status.HTTP_404_NOT_FOUND)
    return Response({''},status=status.HTTP_401_UNAUTHORIZED)

@twofa_required
@login_required()
@api_view(['DELETE'])
def delete_invoice(request):
    invoice_id = request.POST.get('delete_obj_id')
    if request.method == 'DELETE' and request.is_ajax():
        if request.user.is_assistant:
            pass
        else:
            try:
                get_invoice = request.user.all_invoices.get(id=invoice_id)
                get_invoice.delete()
                return Response({'status':'success'},status=status.HTTP_200_OK)
            except:
                return Response({'status':'error'},status=status.HTTP_404_NOT_FOUND)
    return Response({''},status=status.HTTP_401_UNAUTHORIZED)