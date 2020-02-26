from django.db import models

# Create your models here.
class Seasons(models.Model):

    SeasonName = models.CharField(max_length=254, blank=True, null=True)
    StartDate = models.DateField(blank=True)
    EndDate = models.DateField(blank=True, null= True)


class  Customers(models.Model):
    CustomerName = models.CharField(max_length=254, blank=True, null=True)



class CustomerSummaries(models.Model):
    customer =  models.ForeignKey(Customers,on_delete=models.CASCADE)
    season = models.ForeignKey(Seasons, on_delete= models.CASCADE)
    totalRepaid = models.DecimalField(max_digits=19, decimal_places=2)
    totalCredit = models.DecimalField(max_digits=19, decimal_places=2)


class RepaymentUploads(models.Model):
    customer =  models.ForeignKey('Customers', on_delete=models.CASCADE)
    season = models.ForeignKey(Seasons, on_delete= models.CASCADE, blank=True,null=True)
    date =  models.DateField(blank=True, null=True)
    amount = models.DecimalField (max_digits=19, decimal_places=2)


class Repayments(models.Model):
    customer =  models.ForeignKey(Customers, on_delete=models.CASCADE)
    season = models.ForeignKey(Seasons, on_delete= models.CASCADE, blank=True,null=True)
    date =  models.DateField(blank=True, null=True)
    amount = models.DecimalField(max_digits=19, decimal_places=2)
    parent_id = models.IntegerField(blank= True, null=True)
    
    

