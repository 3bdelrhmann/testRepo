from .serializers import GovernorateSerializer,RegionSerializer,LawyersSerializer
from django.contrib.auth.decorators import login_required
from rest_framework.renderers import JSONRenderer
from accounts.models import Governorate,Region
from rest_framework.decorators import api_view
from accounts.models import VerifyLastSentIn
from rest_framework.response import Response
from django.core.paginator import Paginator
from rest_framework  import status
from django.utils    import timezone
from accounts.models import User
from django.db.models import Q

@login_required()
@api_view(('GET',))
def resend_verify_code(request):
    date_now = timezone.now()
    data = {}
    try:
        get_user = request.user
        phone_last = request.user.last_sent
        if phone_last.efforts >= 10:
            data['reminder'] = ''
            data['sent']     = False
            return data
        get_waiting_seconds  = phone_last.efforts * 60
        get_last_sent_seconds = (date_now - phone_last.last_sent).total_seconds()
        if get_last_sent_seconds >= get_waiting_seconds:
            phone_last.efforts = phone_last.efforts + 1
            get_user.send_code = True
            get_user.save()
            phone_last.save()
            data['sent'] = True
            data['reminder'] = phone_last.efforts * 60
            return Response(JSONRenderer().render(data),status=status.HTTP_200_OK)
        else:
            data['sent'] = False
            data['reminder'] = get_waiting_seconds - get_last_sent_seconds
            return Response(JSONRenderer().render(data),status=status.HTTP_200_OK)
    except:
        create = VerifyLastSentIn.objects.create(user=request.user,efforts=1)
        get_user.send_code = True
        get_user.save()
        create.save()
        data['sent'] = True
        data['reminder'] = create.efforts * 60
        return Response(JSONRenderer().render(data),status=status.HTTP_200_OK)

@api_view(['GET'])
def get_governorate(request):
    if request.GET.get('country'):
        country = request.GET.get('country')
        govs    = Governorate.objects.filter(country__id=country)
        serialized_data = GovernorateSerializer(govs,many=True)
        if serialized_data.data:
            return Response(serialized_data.data,status=status.HTTP_200_OK)
        return Response(serialized_data.data,status=status.HTTP_404_NOT_FOUND)
    return HttpResponse('')

@api_view(['GET'])
def get_regions(request):
    if request.GET.get('governorate'):
        governorate = request.GET.get('governorate')
        regions     = Region.objects.filter(governorate__id=governorate)
        serialized_data = RegionSerializer(regions,many=True)
        if serialized_data.data:
            return Response(serialized_data.data,status=status.HTTP_200_OK)
        return Response(serialized_data.data,status=status.HTTP_404_NOT_FOUND)
    return HttpResponse('')

@api_view(['GET'])
def lawyer_search(request):
    if request.method == 'GET' and request.is_ajax():
    # if request.method == 'GET':
        lawyer_name = request.GET.get('lawyer_name')
        governorate = request.GET.get('governorate')
        speicalist  = request.GET.get('speicalist')
        region      = request.GET.get('region')
        page        = request.GET.get('page_num')
        phone_book  = request.GET.get('phone_book')
        onsite_book = request.GET.get('onsite_book')
        data  = User.objects.all().exclude(blocked_booking=True,
            in_review=True,
            is_banned=True,
            is_assistant=True,
            ).order_by('id')
        if phone_book: 
            data = data.filter(
                phone_book=True,
            )
        if onsite_book:
            data = data.filter(
                phone_book=True,
            )

        if governorate:
            data  = data.filter(governorate__name__icontains=governorate)
        if region:
            data  = data.filter(region__name__icontains=region)
        if speicalist:
            data  = data.filter(specialties__name__icontains=speicalist)
        if lawyer_name:
            data  = data.filter(Q(first_name__icontains=lawyer_name) | Q(last_name__icontains=lawyer_name))
            # data  = data.filter(last_name__icontains=lawyer_name)

        if data:
            pagination = Paginator(data,2)
            if int(page) > pagination.num_pages:
                data = {}
            else:
                data = pagination.get_page(page)

        serializer  = LawyersSerializer(data,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    return Response({''},status=status.HTTP_401_UNAUTHORIZED)
