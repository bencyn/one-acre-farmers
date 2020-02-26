from rest_framework import serializers
from .models import Customers , Seasons , CustomerSummaries , RepaymentUploads, Repayments
from django_filters.rest_framework import DjangoFilterBackend

class CustomerSerializer(serializers.ModelSerializer):
    """ Customers Serializer Object"""
    class Meta:
        model = Customers
        fields = '__all__'


class SeasonsSerializer(serializers.ModelSerializer):
    """ Seasons Serializer Object"""
    class Meta:
        model = Seasons
        fields = '__all__'



class CustomerSummariesSerializer(serializers.ModelSerializer):
    """ Customer Summaries"""

    class Meta:
        model = CustomerSummaries
        fields = '__all__'
        

class  RepaymentUploadsSerializer(serializers.ModelSerializer):
    """ Repayment Uploads Object"""

    class Meta:
        model = RepaymentUploads
        fields = '__all__'


class RepaymentsSerializer(serializers.ModelSerializer):
    """Repayment Records Serializer"""

    class Meta:
        model = Repayments
        fields = '__all__'