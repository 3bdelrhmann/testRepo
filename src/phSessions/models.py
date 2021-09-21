from django.db import models
from accounts.models import User,Customer
from django.db.models.signals import post_save
from django.dispatch import receiver
from uuid import uuid4


class phSession(models.Model):
    payment_methods = (
        ('1','credit'),
        ('2','fawry'),)

    id = models.UUIDField(
            primary_key=True,
            default=uuid4,
            editable=False)
    lawyer             = models.ForeignKey(User, on_delete=models.PROTECT)
    customer           = models.ForeignKey(Customer, on_delete=models.PROTECT)
    created_at         = models.DateTimeField(auto_now_add=True)
    session_cost       = models.FloatField(blank=True, null=True)
    payment_method     = models.CharField(choices=payment_methods,max_length=10)
    pocket_money       = models.FloatField(default=0) # 100 | 100

    lawyer_cancel    = models.BooleanField(default=False)
    miss_customer    = models.BooleanField(default=False)
    lawyer_approve   = models.BooleanField(default=False)
    refunded_to_cust = models.BooleanField(default=False)

    pending = models.BooleanField(default=True)
    success = models.BooleanField(default=False)
    closed  = models.BooleanField(default=False)
    paid    = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.lawyer}'

class ChangeLawyerEfforts(models.Model):
    session        = models.ForeignKey(phSession,on_delete=models.CASCADE)
    last_effort_in = models.DateTimeField(auto_now=True) 
    total_efforts  = models.PositiveIntegerField()
    effort_history = models.TextField()

    def __str__(self):
        return self.last_effort_in

class SessionReviews(models.Model):
    session        = models.ForeignKey(phSession,on_delete=models.CASCADE)
    lawyer         = models.ForeignKey(User,on_delete=models.CASCADE,related_name='ph_sessions_reviews')
    customer       = models.ForeignKey(Customer,on_delete=models.CASCADE)
    comment        = models.TextField()
    rate           = models.PositiveIntegerField()
    created_at     = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.session}'
