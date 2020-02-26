from django.shortcuts import render
from rest_framework import viewsets  , status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CustomerSerializer , SeasonsSerializer, CustomerSummariesSerializer, RepaymentUploadsSerializer , RepaymentsSerializer
from .models import Customers , Seasons, CustomerSummaries , RepaymentUploads,Repayments
from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.
class CustomerViewSet(viewsets.ModelViewSet):

    serializer_class = CustomerSerializer
    queryset = Customers.objects.all()

class SeasonsViewSet(viewsets.ModelViewSet):

    serializer_class = SeasonsSerializer
    queryset = Seasons.objects.all()


class CustomerSummariesView(viewsets.ModelViewSet):

    serializer_class = CustomerSummariesSerializer
    queryset =  CustomerSummaries.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['customer', 'season']


class RepaymentsView(viewsets.ModelViewSet):
    serializer_class = RepaymentsSerializer
    queryset = Repayments.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['customer','season','date','amount','parent_id']


class RepaymentUploadsView(APIView):
    # serializer_class = RepaymentUploadsSerializer
    # queryset = RepaymentUploads.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['customer', 'season']


    def get(self,request, format= None):
        """ fetch repayment uploads"""
        rep_uploads = RepaymentUploads.objects.all()
        serializer = RepaymentUploadsSerializer(rep_uploads, many=True)
        return Response(serializer.data)
        

    def post(self,request,fromat= None):
        
        # save repayment upload record
        
        upload_serializer = RepaymentUploadsSerializer(data = request.data)

        if upload_serializer.is_valid():
            upload_serializer.save()
            # return Response(upload_serializer.data, status.HTTP_201_CREATED)
        # get customer

        # cascade repayments
        req_data = self.request.data
        customer = req_data['customer']
        date = req_data['date']
        season = req_data['season']
        payment = req_data['amount']

        print("=== Customer Post", customer)
        credit_records = CustomerSummaries.objects.filter(customer=customer).order_by('id').values()

        recordCounts = len(credit_records)

        # print("Credit Records to", credit_records[0]['totalCredit'])
        print("Credit Records List", credit_records)
        print("Credit Records len", len(credit_records))

        parent_id = None
        # filter credits by customer and get total debt
        initial_amount = payment

        print("Reducing Amount", initial_amount)
        for record in credit_records:
            print("Record",record)

            payment_amount = initial_amount
            print("Reducing Payment",payment_amount)
            # Create Repayment Record
            repayment_record = {
                "date" : req_data['date'],
                "amount": payment_amount,
                "customer": req_data['customer'],
                "season": record['season_id'],
                "parent_id": parent_id
            }

            rp_serializer = RepaymentsSerializer(data = repayment_record)
            rp_serializer.is_valid(raise_exception=True)
            rp_serializer.save()

            # Set Parent Id after first repayment record entry
            parent_id = rp_serializer.data['id']

            print("Repayment Record",rp_serializer.data)

            credit = record['totalCredit']
            currentTotalPaid = record['totalRepaid']

            season_debt = credit - currentTotalPaid
            payment_amount = payment_amount -season_debt
            print("Season Debt", season_debt)
            total_paid = currentTotalPaid + payment_amount

            print("---Total Paid----",total_paid)
            # update customer summaries

            updated_summary = {
                "totalRepaid":total_paid,
            }
            cs_pk = int(record['id'])
            customer_summaries = CustomerSummaries.objects.get(pk=cs_pk)
            print("CustomerSummarry Primary",customer_summaries.pk)
            cs_serializer = CustomerSummariesSerializer(customer_summaries,data=updated_summary,partial = True)

            if cs_serializer.is_valid():
                cs_serializer.save()
                print(cs_serializer.data)
            else:
                print("error")
            if payment_amount < season_debt:
                payment_amount = payment_amount
            else:
                payment_amount = payment_amount - season_debt
                

            print("Reducing Payment",payment_amount)

        message= "okay"
        repayments = Repayments.objects.filter(customer=customer,date=date)
        rep_serializers = RepaymentsSerializer(repayments, many=True)

        cust_summary = CustomerSummaries.objects.filter(customer=customer)
        summary_serializers = CustomerSummariesSerializer(cust_summary, many =True)

        results = {
            "Repayments":rep_serializers.data,
            "Customer Summaries":summary_serializers.data

        }
        return Response(results)

    
    