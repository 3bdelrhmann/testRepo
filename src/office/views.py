from office.forms import InvoiceForm,InvoiceInputsForm,InvoiceFormSet,CustomerIndexForm,AssistantForm,AgendaForm
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,JsonResponse
from rest_framework.renderers import JSONRenderer
from accounts.decorators import twofa_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.forms import modelformset_factory
from django.forms import inlineformset_factory

from office.models import InvoiceInputs,Invoice,InvoiceSetting
from django.shortcuts import render,redirect
from django.urls import reverse,resolve
from rest_framework import status
from django.utils import timezone
from django.db.models import Sum
from django.contrib import messages
from django.utils.timezone import datetime
from accounts.models import User

INVOICE_INPUT_PREFIX = 'InvInput'


@login_required
@twofa_required
def office_home(request):
    context = {
        'title' : 'إدارة المكتب',
    }
    return render(request,'office/office_main.html',context)


@login_required
@twofa_required
def invoices(request):
    template_name = 'office/invoices.html'
    context = {
        'title' : 'الفواتير',
    }
    return render(request,template_name,context)

@login_required
@twofa_required
def create_invoice(request,INVOICE_INPUT_PREFIX=INVOICE_INPUT_PREFIX):
    if request.method == 'POST':
        InvInputsFormSet      = InvoiceFormSet(request.POST,prefix=INVOICE_INPUT_PREFIX)
        create_invoice_form   = \
            InvoiceForm(request.POST,initial={'lawyer_name': request.user.get_full_name,'created_at':timezone.now().date()})
        if InvInputsFormSet.is_valid() and create_invoice_form.is_valid():
            assign_lawyer  = create_invoice_form.save(commit=False)
            assign_invoice = InvInputsFormSet.save(commit=False)
            assign_lawyer.lawyer = request.user
            invoice_detail = assign_lawyer.save()
            for form in assign_invoice:
                form.invoice = assign_lawyer
                form.save()
            return redirect('office:invoice_detail',invoice_id=assign_lawyer.id)
    else:
        InvInputsFormSet    = InvoiceFormSet(queryset=InvoiceInputs.objects.none(),prefix=INVOICE_INPUT_PREFIX)
        create_invoice_form = InvoiceForm(initial={'lawyer_name': request.user.get_full_name,'created_at':timezone.now().date()})

    template_name = 'office/create_invoice.html'
    context = {
        'form'  : create_invoice_form,
        'inv_inputs' : InvInputsFormSet,
        'title'  : 'إنشاء فاتورة',
        'PREFIX' : INVOICE_INPUT_PREFIX,
    }
    return render(request,template_name,context)

@login_required
@twofa_required
def invoice_detail(request,invoice_id):
    try:
        invoice = request.user.all_invoices.prefetch_related('invoice_inputs')\
                .select_related('lawyer','lawyer__country','lawyer__governorate','lawyer__region')\
                .get(id=invoice_id)
        invoice_settings = request.user.invoice_settings
    except Invoice.DoesNotExist:
        return HttpResponse('Not Found Or access Denied')
    except InvoiceSetting.DoesNotExist:
        return HttpResponse('Go to invoice Settings')
    
    invoice_cost = invoice.invoice_inputs.aggregate(Sum('cost'))['cost__sum']
    invoice_cost = invoice_cost if invoice_cost else 0
    tax = (invoice_cost * invoice_settings.taxes_percent) / 100
    invoice_with_tax = tax + invoice_cost

    template_path = 'office/invoice_detail.html'
    context = {
        'tax_percent' : invoice_settings.taxes_percent,
        'tax' : tax,
        'invoice_cost' : invoice_cost,
        'invoice_with_tax' : invoice_with_tax,
        'invoice_settings' : invoice_settings,
        'invoice_detail' : invoice,
        'title' : 'تفاصيل الفاتورة',
    }

    if request.POST.get('DeleteInvoice'):
        messages.success(request,'تم حذف الفاتورة بنجاح')
        invoice.delete()
        return redirect('office:invoices')
    return render(request,template_path,context)


@login_required
@twofa_required
def invoice_update(request,invoice_id,INVOICE_INPUT_PREFIX=INVOICE_INPUT_PREFIX):

    get_inv              = request.user.all_invoices.get(id=invoice_id)
    InvoiceFormInlineSet = inlineformset_factory(Invoice, InvoiceInputs, fields=('invoice','id','title','cost'),extra=0\
        ,can_delete=True)
    InvInputsFormSet     = InvoiceFormInlineSet(instance=get_inv,prefix=INVOICE_INPUT_PREFIX)
    InvoiceForm_instance = InvoiceForm(instance=get_inv)
    if request.method == 'POST':
        InvoiceForm_instance = InvoiceForm(request.POST,instance=get_inv)
        InvInputsFormSet     = InvoiceFormInlineSet(request.POST,instance=get_inv,prefix=INVOICE_INPUT_PREFIX)
        if InvoiceForm_instance.is_valid() and InvInputsFormSet.is_valid():
            InvoiceForm_instance.save()
            InvInputsFormSet.save()
            messages.success(request,"تم التعديل بنجاح")
            return redirect('office:invoice_detail',invoice_id=invoice_id)
    template_path = 'office/update_invoice.html'
    context = {
        'form'  : InvoiceForm_instance,
        'inv_inputs' : InvInputsFormSet,
        'PREFIX' : INVOICE_INPUT_PREFIX,
        'title' : 'تفاصيل الفاتورة'
    }
    return render(request,template_path,context)

@login_required
@twofa_required
def agenda(request):
    template_path = 'office/agenda.html'
    context = {
        'title' : 'جدول الأعمال',
        'today' : datetime.today(),
        # 'tomorrow' : datetime.today() + datetime.timedelta(days=1)
    }

    if request.user.is_assistant:
        pass
    else:
        lawyers        = request.user.lawyer_assistants.all()
        incoming_dates = request.user.lawyer_agenda.all()
        incoming_dates = incoming_dates.filter(session_date__gt=datetime.today()).distinct('session_date')
    context['update_agenda_url'] = reverse('office:update_agenda',kwargs={'agenda_id':'0000'}).replace('0000','')
    print(context['update_agenda_url'])

    context['lawyers'] = lawyers
    context['incoming_dates'] = incoming_dates
    return render(request,template_path,context)


@login_required
@twofa_required
def customer_index(request):
    form = CustomerIndexForm(UserProfile=request.user)
    template_path = 'office/customer_index.html'
    context = {
        'form'  : form,
        'title' : 'فهرس العملاء',
    }
    if request.user.is_assistant:
        pass
    else:
        lawyers = request.user.lawyer_assistants.all()
    update_url = reverse('office:update_client',kwargs={'client_id':'0000'}).replace('0000','')
    context['lawyers'] = lawyers
    context['update_obj_url'] = update_url
    return render(request,template_path,context)

@login_required
@twofa_required
def contract_forms(request):
    template_path = 'office/contract_forms.html'
    context = {
        'title' : 'نماذج العقود',
    }
    return render(request,template_path,context)


@login_required
@twofa_required
def manage_assistants(request):
    form = AssistantForm()
    template_path = 'office/manage_assistants.html'
    tmp_uuid         = 'c315e5b8-f8de-4903-b888-108b8e7e7d98'

    context = {
        'form'  : form,
        'title' : 'إدارة الموظفين',
        'update_assistant_url': reverse('office:update_assistant',kwargs={'assistant_id':tmp_uuid}).replace(tmp_uuid,'')
    }
    return render(request,template_path,context)


@login_required
@twofa_required
def create_agenda(request):
    form = AgendaForm(user=request.user)
    if  request.method == 'POST':
        form = AgendaForm(user=request.user, data=request.POST)
        if form.is_valid():
            add_lawyer = form.save(commit=False)
            add_lawyer.lawyer = request.user
            add_lawyer.save()
            messages.success(request,'تم إضافة جلسة جديدة بنجاح')
            return redirect("office:created_agenda", agenda_id = add_lawyer.id)
        # redirect to created agenda page
    template_path = 'office/create_agenda.html'
    context = {
        'form'  : form,
        'title' : 'إضافة مهمة جديدة',
    }
    return render(request,template_path,context)
@login_required
@twofa_required
def update_agenda(request,agenda_id):
    # handle error if access denied
    get_agenda_data = request.user.lawyer_agenda.get(id=agenda_id)
    context = {}
    form = AgendaForm(user=request.user,instance=get_agenda_data)
    if request.method == 'POST':
        form = AgendaForm(request.POST,user=request.user,instance=get_agenda_data)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم التعديل بنجاح')
            print("SUCCCESS")
            return redirect("office:created_agenda",agenda_id=get_agenda_data.id)
            
    context['title'] =  'تعديل جدول الأعمال'
    context['form'] =  form
    template_path = 'office/update_agenda.html'
    return render(request,template_path,context)

@login_required
@twofa_required
def created_agenda(request,agenda_id):
    context = {}
    try:
        get_agenda = request.user.lawyer_agenda.get(id=agenda_id)
        context['agenda_detail'] = get_agenda
    except:
        return redirect('office:agenda')

    if request.method == 'POST':
        if request.POST.get('DeleteCustomerConfirmation') == 'true':
            get_agenda.delete()
            messages.success(request, 'تم الحذف من جدول الاعمال بنجاح')
            return redirect('office:agenda')

    context['title'] =  'تفاصيل الجلسة'
    template_path = 'office/created_agenda.html'
    return render(request,template_path,context)

@login_required
@twofa_required
def create_client(request):
    context = {}
    form = CustomerIndexForm(request.user)
    context['title'] =  'إضافة عميل جديد'
    context['form'] =  form
    template_path = 'office/create_customer.html'
    return render(request,template_path,context)


@login_required
@twofa_required
def update_client(request,client_id):
    # handle error if access denied
    get_client_data = request.user.lawyer_customers.get(id=client_id)
    context = {}
    form = CustomerIndexForm(UserProfile=request.user,instance=get_client_data)
    if request.method == 'POST':
        form = CustomerIndexForm(request.POST,UserProfile=request.user,instance=get_client_data)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تعديل بيانات العميل بنجاح')
            return redirect('office:created_customer',get_client_data.id)
        # else:
        #     print(form.errors)
        #     # context['errors'] = nw_form.error_class;
    context['title'] =  'تعديل بيانات العميل'
    context['form'] =  form
    template_path = 'office/update_customer.html'
    return render(request,template_path,context)

@login_required
@twofa_required
def created_customer(request,client_id):
    context = {}
    if not client_id:
        return redirect('office:clients')
    try:
        get_customer = request.user.lawyer_customers.get(id=client_id)
        context['customer_detail'] = get_customer
    except:
        return redirect('office:clients')
    if request.method == 'POST':
        if request.POST.get('DeleteCustomerConfirmation') == 'true':
            get_customer.delete()
            messages.success(request, 'تم حذف العميل بنجاح')
            return redirect('office:clients')
    context['title'] =  'تفاصيل العميل'
    template_path = 'office/created_customer.html'
    return render(request,template_path,context)


@login_required
@twofa_required
def create_assistant(request):
    context = {}
    # AssistantForm
    form = AssistantForm()
    tmp_uuid         = 'c315e5b8-f8de-4903-b888-108b8e7e7d98'
    context['title'] =  'إضافة محامي جديد'
    context['created_assistant_url']    = reverse('office:created_assistant',kwargs={'assistant_id':tmp_uuid}).replace(tmp_uuid,'')
    context['form'] =  form
    template_path = 'office/create_assistant.html'
    return render(request,template_path,context)


@login_required
@twofa_required
def created_assistant(request,assistant_id):
    context = {}
    get_assistant = request.user.lawyer_assistants.get(id=assistant_id)
    context['assistant_detail'] = get_assistant
    if request.method == 'POST':
        if request.POST.get('DeleteCustomerConfirmation') == 'true':
            get_assistant.delete()
            messages.success(request, 'تم حذف المحامي بنجاح')
            return redirect('office:manage_assistants')
    context['title'] =  'تم إضافة محامي جديد بنجاح'
    template_path = 'office/created_assistant.html'
    return render(request,template_path,context)


@login_required
@twofa_required
def update_assistant(request,assistant_id):
    # handle error if access denied
    get_assistant = request.user.lawyer_assistants.get(id=assistant_id)
    context = {}
    form = AssistantForm(instance=get_assistant)
    if request.method == 'POST':
        form = AssistantForm(request.POST,instance=get_assistant)
        if form.is_valid():
            nw_form = form.save(commit=False)
            nw_form.assistant_to = request.user
            print('Success')
            nw_form.save()
            messages.success(request, 'تم تعديل بيانات المحامي بنجاح')
            return redirect('office:created_assistant',get_assistant.id)
    context['title'] =  'تعديل بيانات المحامي'
    context['form'] =  form
    template_path = 'office/update_assistant.html'
    return render(request,template_path,context)
