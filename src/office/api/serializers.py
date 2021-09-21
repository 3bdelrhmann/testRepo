from office.models import Invoice,Agenda,CustomerIndex,ContractsForms
from rest_framework import serializers
from accounts.models import User

class InvoiceSerializer(serializers.ModelSerializer):
    created_at = serializers.DateField(format="%Y|%b-%d")
    class Meta:
        model = Invoice
        fields = '__all__'

class AgendaSerializer(serializers.ModelSerializer):
    session_date = serializers.DateField(format="%Y|%b-%d")
    class Meta:
        model = Agenda
        fields = '__all__'

class CustomerIndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerIndex
        fields = '__all__'

class ContractsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractsForms
        fields = '__all__'

class AsistantSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
                'allow_assistant_update',
                'allow_assistant_delete',
                'allow_assistant_add',
                'data_is_restricted',
                'is_assistant',
                'assistant_to',
                'first_name',
                'last_name',
                'password',
                'email',
                'id',
                ]