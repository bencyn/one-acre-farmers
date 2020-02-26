from django.shortcuts import render
from rest_framework import viewsets  , status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import (CustomerSerializer, SeasonsSerializer,
                        CustomerSummariesSerializer,RepaymentUploadsSerializer , 
                        RepaymentsSerializer )
from .models import Customers , Seasons, CustomerSummaries , RepaymentUploads,Repayments
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, F
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
        repayment_upload = RepaymentUploadsSerializer(data = request.data)

        if repayment_upload.is_valid():
            repayment_upload.save()
        else:
            return Response(repayment_upload.errors, status=status.HTTP_400_BAD_REQUEST)
       
        # cascade repayments
        req_data = self.request.data
        customer = req_data['customer']
        date = req_data['date']
        season = req_data['season']
        payment = req_data['amount'] 

        parent_id = None
        # overpaid 
        # get total credit and totalRepaid
        # if totalRepaid == total credit
        # add new customer summary
        cs_instance = CustomerSummaries.objects.filter(customer=customer)
    
        # get customer summary based on request data
        

        total_repaid_sum = cs_instance.aggregate(total=Sum('totalRepaid'))
        total_credit_sum = cs_instance.aggregate(total=Sum('totalCredit'))
        print("==tr",total_repaid_sum['total'])
        print("==tc",total_credit_sum)
        

        # overpaid case 
        total_debt = total_credit_sum['total'] - total_repaid_sum['total']
        print("==total debt", total_debt)
        if total_debt == 0:
            # create a new repayment record
            cust_summary = CustomerSummaries.objects.filter(customer=customer).latest('season')

            print("==latestRecord", cust_summary.season.pk)
            repayment_record = {
                    "date" : req_data['date'],
                    "amount": payment,
                    "customer": req_data['customer'],
                    "season": cust_summary.season.pk,
                    "parent_id": parent_id
                }

            rp_serializer = RepaymentsSerializer(data = repayment_record)
            rp_serializer.is_valid(raise_exception=True)
            rp_serializer.save()

            # get customer summaries

            cust_summary = CustomerSummaries.objects.filter(customer=customer)
            summary_serializers = CustomerSummariesSerializer(cust_summary, many =True)
            results = {
                "RepaymentUpload":repayment_upload.data,
                "RepaymentRecord":rp_serializer.data,
                "CustomerSummaries":summary_serializers.data
            }

            return Response(results)
        # overide case
        if season:
            
            cust_summary = CustomerSummaries.objects.get(season=season,customer=customer)
           
            # create repaymet record
            
            repayment_record = {
                    "date" : req_data['date'],
                    "amount": payment,
                    "customer": req_data['customer'],
                    "season": cust_summary.season.pk,
                    "parent_id": parent_id
                }

            rp_serializer = RepaymentsSerializer(data = repayment_record)
            rp_serializer.is_valid(raise_exception=True)
            rp_serializer.save()


            # update customer summary
            debt = cust_summary.totalCredit - cust_summary.totalRepaid

            if payment > debt:
                totalRepaid = cust_summary.totalCredit
            else:
                totalRepaid = cust_summary.totalRepaid + payment

        
            # update customer summary
            updated_summary = {
                "totalRepaid":totalRepaid,
            }
           
            cs_serializer = CustomerSummariesSerializer(cust_summary,data=updated_summary,partial = True)
            if cs_serializer.is_valid():
                cs_serializer.save()
            
            # display all results
                results = {
                    "RepaymentUpload":repayment_upload.data,
                    "RepaymentRecord":rp_serializer.data,
                    "CustomerSummary": cs_serializer.data

                }

                return Response(results)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # cascade case
        elif not season and total_debt > 0:
            
            # create initial repayment record
            # get first season
            cs_credit_instance = CustomerSummaries.objects.filter(customer=customer,totalRepaid__lt=F('totalCredit')).order_by('id','season')
            
            oldest_credit = cs_credit_instance.first()
        
            # create initial repayment record
            repayment_record = {
                    "date" : req_data['date'],
                    "amount": payment,
                    "customer": req_data['customer'],
                    "season": oldest_credit.season.pk,
                    "parent_id": parent_id
                }

            rp_serializer = RepaymentsSerializer(data = repayment_record)
            rp_serializer.is_valid(raise_exception=True)
            rp_serializer.save()
            
            parent_id = rp_serializer.data['id']

            old_record_debt = oldest_credit.totalCredit - oldest_credit.totalRepaid
            adjusted_payment = old_record_debt - payment
            credit_records = cs_credit_instance.order_by('id').values()
            
            print("credit records",credit_records)

            count = 0
            for record in credit_records:
               
                count = count +1
                print("==== {} adjusted amount".format(count),abs(adjusted_payment))
                # create adjustment repayment records
                repayment_record = {
                    "date" : req_data['date'],
                    "amount":  adjusted_payment,
                    "customer": req_data['customer'],
                    "season": record['season_id'],
                    "parent_id": parent_id
                }

                rp_serializer = RepaymentsSerializer(data = repayment_record)
                rp_serializer.is_valid(raise_exception=True)
                rp_serializer.save()

                # fix amount signs bug

                # update customer summary
                record_debt = record['totalCredit'] - record['totalRepaid']
                
                print("=== {} Record Debt".format(count), record_debt)
                if abs(adjusted_payment) > record_debt:
                    totalRepaid = record['totalCredit']
                else:
                    totalRepaid = record['totalRepaid'] + abs(adjusted_payment)

                updated_summary = {
                    "totalRepaid":totalRepaid,
                }

                cs_pk = int(record['id'])
                customer_summaries = CustomerSummaries.objects.get(pk=cs_pk)
                cs_serializer = CustomerSummariesSerializer(customer_summaries,data=updated_summary,partial = True)

                if cs_serializer.is_valid():
                    cs_serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
                adjusted_payment = record_debt - abs( adjusted_payment)

            repayments = Repayments.objects.filter(customer=customer,date=date)
            rep_serializers = RepaymentsSerializer(repayments, many=True)

            cust_summary = CustomerSummaries.objects.filter(customer=customer)
            summary_serializers = CustomerSummariesSerializer(cust_summary, many =True)

            results = {
                "RepaymentUpload":repayment_upload.data,
                "RepaymentRecord":rep_serializers.data,
                "CustomerSummaries":summary_serializers.data

            }

            return Response(results)

    
    