from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

from apps.customers.models import Customer
from .models import Loan
from .serializers import (
    LoanEligibilitySerializer, LoanEligibilityResponseSerializer,
    LoanCreationSerializer, LoanCreationResponseSerializer,
    LoanDetailSerializer, CustomerLoanSerializer
)
from .utils import check_loan_eligibility, calculate_monthly_installment

@api_view(['POST'])
def check_eligibility(request):
    serializer = LoanEligibilitySerializer(data=request.data)
    if serializer.is_valid():
        eligibility_data = check_loan_eligibility(**serializer.validated_data)
        response_serializer = LoanEligibilityResponseSerializer(eligibility_data)
        return Response(response_serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_loan(request):
    serializer = LoanCreationSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data
        eligibility = check_loan_eligibility(**data)
        
        if not eligibility['approval']:
            return Response({
                'loan_id': None,
                'customer_id': data['customer_id'],
                'loan_approved': False,
                'message': 'Loan not approved based on credit score and eligibility criteria',
                'monthly_installment': eligibility['monthly_installment']
            })
        
        try:
            customer = Customer.objects.get(customer_id=data['customer_id'])
            
            # Create loan with corrected interest rate
            start_date = date.today()
            end_date = start_date + relativedelta(months=data['tenure'])
            monthly_installment = calculate_monthly_installment(
                data['loan_amount'], 
                eligibility['corrected_interest_rate'], 
                data['tenure']
            )
            
            loan = Loan.objects.create(
                customer=customer,
                loan_amount=data['loan_amount'],
                tenure=data['tenure'],
                interest_rate=eligibility['corrected_interest_rate'],
                monthly_repayment=monthly_installment,
                start_date=start_date,
                end_date=end_date
            )
            
            return Response({
                'loan_id': loan.loan_id,
                'customer_id': data['customer_id'],
                'loan_approved': True,
                'message': 'Loan approved successfully',
                'monthly_installment': monthly_installment
            })
            
        except Customer.DoesNotExist:
            return Response({
                'loan_id': None,
                'customer_id': data['customer_id'],
                'loan_approved': False,
                'message': 'Customer not found',
                'monthly_installment': 0
            })
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def view_loan(request, loan_id):
    try:
        loan = Loan.objects.select_related('customer').get(loan_id=loan_id)
        serializer = LoanDetailSerializer(loan)
        return Response(serializer.data)
    except Loan.DoesNotExist:
        return Response({'error': 'Loan not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def view_loans_by_customer(request, customer_id):
    try:
        customer = Customer.objects.get(customer_id=customer_id)
        loans = Loan.objects.filter(customer=customer)
        serializer = CustomerLoanSerializer(loans, many=True)
        return Response(serializer.data)
    except Customer.DoesNotExist:
        return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)
