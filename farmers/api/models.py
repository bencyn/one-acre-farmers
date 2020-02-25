from django.db import models

# Create your models here.
class Seasons(models.Model):

    seasonName = models.CharField(max_length=254, blank=True, null=True)
    startDate = models.DateTimeField(blank=True, null=True)
    endDate = models.DateTimeField(blank=True, null=True)


class  Customers(models.Model):
    customerName = models.CharField(max_length=254, blank=True, null=True)



class CustomerSummaries(models.Model):
    customer =  models.ForeignKey(Customers, on_delete=models.CASCADE)
    season = models.ForeignKey(Seasons, on_delete= models.CASCADE)
    totalRepaid = models.DecimalField(..., max_digits=19, decimal_places=10)
    totalCredit = models.DecimalField(..., max_digits=19, decimal_places=10)


class RepaymenUploads(models.Model):
    customer =  models.ForeignKey(Customers, on_delete=models.CASCADE)
    season = models.ForeignKey(Seasons, on_delete= models.CASCADE, blank=True,null=True)
