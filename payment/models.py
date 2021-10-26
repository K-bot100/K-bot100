from django.db import models
from django.utils import timezone
from requests.api import request


# Create your models here.

class Payments(models.Model):
    date = models.DateTimeField(default=timezone.now)
    name = models.CharField(max_length=255,null=True,blank=True)
    transactionId = models.CharField(max_length=200,null=True,blank=True,verbose_name='transactionId')
    extid = models.CharField(max_length=200,null=True,blank=True)
    amountPaid = models.CharField(max_length=10,null=True,blank=True,verbose_name='amountPaid')
    phoneNumber=models.CharField(max_length=20,null=True,blank=True,verbose_name='phoneNumber')
    productType=models.CharField(max_length=20,null=True,blank=True,verbose_name='productType')
    numberOfBuckets=models.CharField(max_length=200,null=True,blank=True,verbose_name='paymentRemarks')
    reason=models.CharField(max_length=150,null=True,blank=True)
    status=models.CharField(max_length=50,null=True,blank=True)
    community=models.CharField(max_length=50,null=True,blank=True,verbose_name='community')
    paid_by=models.CharField(max_length=50,null=True,blank=True,verbose_name='Paid By')

    def __str__(self):
        return str(self.name) + " payment " + str(self.date)