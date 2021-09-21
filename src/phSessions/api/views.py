from django.http       import HttpResponse,JsonResponse
from accounts.forms    import CreateCustomer
from phSessions.models import phSession

from django.core.paginator import Paginator

from django.shortcuts import redirect
from accounts.models  import Customer
from django.shortcuts import render
from accounts.models  import User

from rest_framework   import status
from rest_framework.renderers  import JSONRenderer
from rest_framework.response   import Response
from rest_framework.decorators import api_view

from phSessions.api.serializers import SessionsReviewsSerializer

@api_view(('POST',))
def book_PhSession(request):
    if not request.method == 'POST':
        return redirect('home')
    payment_method = request.POST.get('payment_method')
    
    if not payment_method: # 0b2e8448-254d-492b-9eb4-aa78d9893bb8
        data = {'payment_method':[{'message':'رجاءًا إختر وسيلة الدفع'}]}
        return Response(JSONRenderer().render(data),status=status.HTTP_422_UNPROCESSABLE_ENTITY) # The alternative of these create a form-"class" with phSession-"model" and send request.POST to the form class and the form will check if is empty or not
        # so, i wrote these code to shortcut these long process 
    form = CreateCustomer(request.POST)
    if form.is_valid():
        customer = form.save()
    elif form.has_error('mobile_number',code='unique'):
        customer = Customer.objects.get(mobile_number=request.POST.get('mobile_number'))
    else:
        return Response(form.errors.as_json(),status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    try:
        lawyer  = User.objects.get(id=request.POST.get('lawyer_id'))
    except:
        return HttpResponse('Lawyer not found')
    

    create_session = phSession.objects.create(lawyer=lawyer,customer=customer,\
        session_cost=lawyer.phone_cost,payment_method=payment_method,\
        pocket_money=lawyer.phone_cost,paid=True) ##- until integrate with payment gateway
    create_session.save()
    
    data = {'session_id' : create_session.id,'created':True}
    return Response(JSONRenderer().render(data),status=status.HTTP_201_CREATED)


@api_view(('GET',))
def get_lawyer_reviews(request):
    if request.method == 'GET' and request.is_ajax():
        lawyer_id   = request.GET.get('lawyer_id')
        page_number = request.GET.get('page_num')
        try:
            get_lawyer  = User.objects.get(id=lawyer_id)
        except User.DoesNotExist:
            return Response({''},status=status.HTTP_404_NOT_FOUND)    
        data = get_lawyer.ph_sessions_reviews.all()
        
        pagination = Paginator(data,10)
        if int(page_number) > pagination.num_pages:
            data = {} # to skip repeat last result
        else:
            data = pagination.get_page(page_number)
        serializer = SessionsReviewsSerializer(data,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    return Response({''},status=status.HTTP_401_UNAUTHORIZED)    
