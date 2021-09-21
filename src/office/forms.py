from office.models import Invoice,InvoiceInputs,InvoiceTypes,CustomerIndex,Agenda
from django.forms import modelformset_factory
from accounts.models import User
from django import forms

class InvoiceForm(forms.ModelForm):        
    invoice_type  = forms.ModelChoiceField(queryset=InvoiceTypes.objects.all(),required=True,widget=forms.Select(attrs={
        'class' : 'form-control',
    }))
    class Meta:
        model   = Invoice
        fields  = ['invoice_type','lawyer_name','created_at','file_id','invoice_title','customer_name']
        widgets = {
            'lawyer_name' : forms.TextInput(attrs={
                'class' : 'mb-3 select_all form-control',
            }),
            'created_at' : forms.TextInput(attrs={
                'class' : 'mb-3 invoice_date form-control',
                'autocomplete' : 'off'
            }),
            'file_id' : forms.TextInput(attrs={
                'class' : 'mb-3 form-control',
                'autocomplete' : 'off'
            }),
            'invoice_title' : forms.TextInput(attrs={
                'class' : 'mb-3 form-control',
                'autocomplete' : 'off'
            }),
            'customer_name' : forms.TextInput(attrs={
                'class' : 'mb-3 form-control',
                'autocomplete' : 'off'
            }),}

class InvoiceInputsForm(forms.ModelForm):
    title = forms.CharField(max_length=150,required=True,
        widget=forms.TextInput(attrs={
            'class' : 'item-title mb-3 form-control',
            'autocomplete' : 'off',
        })
    )
    cost  = forms.FloatField(required=True,
        widget=forms.NumberInput(attrs={
            'class' : 'item-cost mb-3 form-control',
        })
    )
    class Meta:
        model   = InvoiceInputs
        fields  = ['title','cost']

InvoiceFormSet = modelformset_factory(InvoiceInputs,
    form=InvoiceInputsForm,
    can_delete=True,
    fields=['title','cost','invoice'])

class CustomerIndexForm(forms.ModelForm):
    class Meta:
        model   = CustomerIndex
        fields  = ['customer_mobile','customer_name','file_id','notes','assign_to']
        widgets = {
            'customer_mobile' : forms.TextInput(
                attrs={
                    'class' : 'form-control',
                    'autocomplete' : 'off',
                }
            ),
            'customer_name'   : forms.TextInput(
                attrs={
                    'class' : 'form-control',
                    'autocomplete' : 'off',
                }
            ),
            'file_id'   :  forms.TextInput(
                attrs={
                    'class' : 'form-control',
                    'autocomplete' : 'off',
                }
            ),
            'notes'     :  forms.Textarea(
                attrs={
                    'rows'  : 3,
                    'class' : 'form-control',
                    'autocomplete' : 'off',
                }
            ),
            'assign_to' : forms.Select(
                attrs={
                    'class' : 'form-control',
                }
            ),
        }
        error_messages = {
            'customer_name' : {
                'required' : 'إسم العميل مطلوب'
            },
            'customer_mobile' : {
                'required' : 'رقم هاتف العميل مطلوب'
            },
            'file_id' : {
                'required' : 'رقم الملف الخاص بالعميل مطلوب'
            }
        }
    def __init__(self,*args,**kwargs):
        current_user = kwargs.pop('UserProfile')
        super(CustomerIndexForm, self).__init__(*args, **kwargs)
        self.fields['assign_to'].queryset = current_user.lawyer_assistants.values_list('first_name','id')


class AssistantForm(forms.ModelForm):
    class Meta:
        model   = User
        fields  = ['first_name','last_name','email','password']

    first_name   = forms.CharField(max_length=100,required=True,widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder':'الأول',
    }),error_messages = {
            'required' : 'رجاءًا قم بكتابة أسمك'})
    last_name    = forms.CharField(max_length=100,required=True,widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder':'اسم العائلة \ اللقب',
    }),error_messages = {
            'required' : 'رجاءًا قم بكتابة اسم العائلة او اللقب'})
    email        = forms.EmailField(required=True,widget=forms.EmailInput(attrs={
        'class' : 'form-control',
        'style' : 'direction:ltr',
        'autocomplete' : 'off',
    }),error_messages = {
            'invalid'  : 'البريد الإلكتروني غير صالح',
            'unique'   : 'مُستخدم اخر يستخدم هذا البريد الإلكتروني رجاءًا قم بتغييره',
            'required' : 'رجاءًا قم بكتابة البريد الإلكتروني الخاص بك'})
    password     = forms.CharField(min_length=8,max_length=255,required=True,widget=forms.PasswordInput(attrs={
        'class' : 'form-control',
        'placeholder':'•••••••••••••',
        'autocomplete' : 'new-password',

    }),error_messages = {
            'invalid'    : 'البريد الإلكتروني غير صالح',
            'min_length' : 'يجب ان تكون كلمة السر على الأقل مكونة من 8 أحرف',
            'required'   : 'رجاءًا قم بكتابة كلمة السر الخاصة بك'})

    # assistant_to  = forms.CharField(widget=forms.HiddenInput())
    class Meta:
        model = User
        fields = ['first_name',
                'last_name',
                'email',
                'password',
                'is_assistant',
                'assistant_to',
                'allow_assistant_update',
                'allow_assistant_delete',
                'allow_assistant_add',
                'data_is_restricted']
        # widgets = {
        #     'allow_assistant_update' : forms.CheckboxInput(attrs={
        #         'class' : 'form-check-input'
        #     })
        # }
    

    # def clean_first_name(self):
    #     first_name = self.cleaned_data['first_name']
    #     full_name = first_name + self.last_name_
    #     return full_name


class AgendaForm(forms.ModelForm):
    class Meta:
        model   = Agenda
        fields  = [
                    'customer_name',
                    'customer_mobile',
                    'session_date',
                    'assign_to',
                    'case_year',
                    'case_id',
                    'court',
                    'notes']
        widgets = {
            'customer_mobile' : forms.TextInput(
                attrs={
                    'class' : 'form-control',
                    'autocomplete' : 'off',
                }
            ),
            'customer_name'   : forms.TextInput(
                attrs={
                    'class' : 'form-control',
                    'autocomplete' : 'off',
                }
            ),
            'session_date'   : forms.TextInput(
                attrs={
                    'autocomplete' : 'off',
                    'class'        : 'form-control',
                    'id'           : 'session_date',
                }
            ),

            'assign_to' : forms.Select(
                attrs={
                    'class' : 'form-control',
                    'id'    : 'assign_to',
                }
            ),

            'case_id'   :  forms.TextInput(
                attrs={
                    'class' : 'form-control',
                    'id'    : 'case_id',
                    'autocomplete' : 'off',
                    'placeholder'  : 'رقم القضية',
                }
            ),
            'case_year' :  forms.TextInput(
                attrs={
                    'class' : 'form-control',
                    'autocomplete' : 'off',
                }
            ),
            'court'     :  forms.TextInput(
                attrs={
                    'class' : 'form-control',
                    'id'    : 'court_name',
                    'placeholder'  : 'إسم المحكمة',
                }
            ),
            'notes'     :  forms.Textarea(
                attrs={
                    'rows'  : 3,
                    'class' : 'form-control',
                    'autocomplete' : 'off',
                }
            ),
        }
        error_messages = {
            'court' : {
                'required' : 'إسم المحكمة مطلوب'
            },
            'case_id' : {
                'required' : 'رقم القضية مطلوب'
            },
            'case_year' : {
                'required' : 'عام القضية مطلوب'
            }
        }
    def __init__(self,*args,**kwargs):
        user = kwargs.pop('user')
        super(AgendaForm, self).__init__(*args, **kwargs)
        self.fields['assign_to'].queryset = user.lawyer_assistants.values_list('first_name',flat=True)

# class CustomerForm(forms.ModelForm):
#     class Meta:
#         model   = CustomerIndex
#         fields  = [
#                     'customer_name',
#                     'customer_mobile',
#                     'assign_to',
#                     'file_id',
#                     'notes']
#         widgets = {
#             'customer_mobile' : forms.TextInput(
#                 attrs={
#                     'class' : 'form-control',
#                     'autocomplete' : 'off',
#                 }
#             ),
#             'customer_name'   : forms.TextInput(
#                 attrs={
#                     'class' : 'form-control',
#                     'autocomplete' : 'off',
#                 }
#             ),
#             'assign_to' : forms.Select(
#                 attrs={
#                     'class' : 'form-control',
#                     'id'    : 'assign_to',
#                 }
#             ),
#         }
#     def __init__(self, user, *args, **kwargs):
#         super(CustomerForm, self).__init__(*args, **kwargs)
#         self.fields['assign_to'].queryset = user.lawyer_assistants.values_list('first_name',flat=True)
