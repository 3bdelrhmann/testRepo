from django.core.validators import RegexValidator,FileExtensionValidator
from tinymce.models import HTMLField
from accounts.models import User
from django.db import models


class InvoiceSetting(models.Model):
    lawyer = models.OneToOneField(User,models.CASCADE,related_name='invoice_settings')
    office_title  = models.CharField(verbose_name='إسم المكتب',max_length=250)
    office_logo   = models.ImageField(verbose_name='شعار المكتب',blank=True)
    taxes_percent = models.FloatField(verbose_name='النسبة المئوية للضرائب',default=0,help_text='سيتم حساب النسبة المئوية التي ستدخلها من كل فاتورة وإضافتها الي مجموع تكلفة الفاتورة')
    def __str__(self):
        return f'{self.lawyer}'
    class Meta:
        verbose_name        = 'إعدادات الفواتير'
        verbose_name_plural = 'إعدادات الفواتير'

class InvoiceTypes(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(allow_unicode=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name        = 'انواع القضايا'
        verbose_name_plural = 'انواع القضايا'

class Invoice(models.Model):
    lawyer        = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name='all_invoices')
    lawyer_name   = models.CharField(verbose_name='إسم المحامي',max_length=150)
    created_at    = models.DateField(verbose_name='تاريخ الفاتورة')
    registered_at = models.DateField(auto_now_add=True)
    invoice_type  = models.ForeignKey(verbose_name='نوع القضية',to=InvoiceTypes,on_delete=models.SET_NULL,null=True)
    invoice_title = models.CharField(verbose_name='عنوان الفاتورة',max_length=100,blank=True) 
    customer_name = models.CharField(verbose_name='إسم الموكل',max_length=150,blank=True)
    file_id       = models.CharField(verbose_name='رقم الملف',max_length=50,blank=True)

    def __str__(self):
        return f'{self.lawyer}'

    def invoice_url(self):
        return self.id
    class Meta:
        verbose_name        = 'الفواتير'
        verbose_name_plural = 'الفواتير'

class InvoiceInputs(models.Model):
    invoice = models.ForeignKey(Invoice,models.CASCADE,null=True,blank=True,related_name='invoice_inputs')
    title   = models.CharField(verbose_name='البند',max_length=50)
    cost    = models.FloatField(verbose_name='التكلفة')
    
    def __str__(self):
        return f'{self.invoice}'
    class Meta:
        verbose_name        = 'بند'
        verbose_name_plural = 'بنود الفواتير'

class Agenda(models.Model):
    lawyer     = models.ForeignKey(User,on_delete=models.CASCADE,related_name='lawyer_agenda')
    assign_to  = models.ForeignKey(User ,on_delete=models.CASCADE,related_name='agenda_assigned',blank=True,null=True)
    created_at   = models.DateField(auto_now_add=True)
    session_date = models.DateField()
    case_id    = models.CharField(max_length=100)
    case_year  = models.CharField(max_length=4) # هنبقا نغيرها في سنة 10 الاف بقا ان شاء الله :"
    court      = models.CharField(max_length=100)
    notes      = models.TextField(blank=True)
    customer_name   = models.CharField(blank=True,max_length=100)
    customer_mobile = models.CharField(blank=True,max_length=15,validators=[RegexValidator(regex='^[0][1][2?0?5?1]\d{8}$',message='رقم الهاتف غير صحيح')])
    def __str__(self):
        return self.case_id

class CustomerIndex(models.Model):
    lawyer    = models.ForeignKey(User,on_delete=models.CASCADE,related_name='lawyer_customers')
    assign_to = models.ForeignKey(User ,on_delete=models.CASCADE,related_name='customers_assigned',blank=True,null=True)
    
    notes     = models.TextField(blank=True)
    file_id   = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    customer_name   = models.CharField(max_length=100)
    customer_mobile = models.CharField(max_length=15,validators=[RegexValidator(regex='^[0][1][2?0?5?1]\d{8}$',message='رقم الهاتف غير صحيح')])
    def __str__(self):
        return self.customer_name
    
class ContractsForms(models.Model):
    lawyer   = models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE,related_name='lawyer_contracts')
    title    = models.CharField(max_length=150)
    contract = HTMLField()
    contract_file = models.FileField(upload_to='contracts/', validators=[
                                    FileExtensionValidator(['docm', 'doc', 'dot', 'pdf', 'docx', 'rtf'])])
    def __str__(self):
        return self.title