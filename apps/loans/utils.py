from datetime import date, datetime
from decimal import Decimal
from apps.customers.models import Customer
from .models import Loan

def calculate_monthly_installment(loan_amount, interest_rate, tenure):
    """Calculate EMI using compound interest formula"""
    monthly_rate = interest_rate / (12 * 100)  # Monthly interest rate
    if monthly_rate == 0:
        return loan_amount / tenure
    
    emi = (loan_amount * monthly_rate * (1 + monthly_rate)**tenure) / ((1 + monthly_rate)**tenure - 1)
    return round(emi, 2)

def calculate_credit_score(customer_id):
    """Calculate credit score based on loan history"""
    try:
        customer = Customer.objects.get(customer_id=customer_id)
    except Customer.DoesNotExist:
        return 0
    
    loans = Loan.objects.filter(customer=customer)
    
    if not loans.exists():
        return 50  # Default score for new customers
    
    # Component 1: Past loans paid on time (40% weight)
    total_emis = sum(loan.tenure for loan in loans)
    total_paid_on_time = sum(loan.emis_paid_on_time for loan in loans)
    on_time_ratio = total_paid_on_time / total_emis if total_emis > 0 else 0
    on_time_score = on_time_ratio * 40
    
    # Component 2: Number of loans taken (20% weight)
    num_loans = loans.count()
    if num_loans <= 2:
        loan_count_score = 20
    elif num_loans <= 5:
        loan_count_score = 15
    else:
        loan_count_score = 10
    
    # Component 3: Loan activity in current year (20% weight)
    current_year = date.today().year
    current_year_loans = loans.filter(start_date__year=current_year)
    if current_year_loans.count() == 0:
        activity_score = 20
    elif current_year_loans.count() <= 2:
        activity_score = 15
    else:
        activity_score = 5
    
    # Component 4: Loan approved volume vs limit (20% weight)
    total_loan_amount = sum(loan.loan_amount for loan in loans)
    volume_ratio = total_loan_amount / customer.approved_limit if customer.approved_limit > 0 else 1
    if volume_ratio <= 0.5:
        volume_score = 20
    elif volume_ratio <= 0.8:
        volume_score = 15
    else:
        volume_score = 5
    
    # Component 5: Current debt vs approved limit
    current_loans = loans.filter(end_date__gte=date.today())
    current_debt = sum(loan.loan_amount for loan in current_loans)
    
    if current_debt > customer.approved_limit:
        return 0
    
    credit_score = on_time_score + loan_count_score + activity_score + volume_score
    return min(100, max(0, credit_score))

def check_loan_eligibility(customer_id, loan_amount, interest_rate, tenure):
    """Check loan eligibility and return approval details"""
    try:
        customer = Customer.objects.get(customer_id=customer_id)
    except Customer.DoesNotExist:
        return {
            'customer_id': customer_id,
            'approval': False,
            'interest_rate': interest_rate,
            'corrected_interest_rate': interest_rate,
            'tenure': tenure,
            'monthly_installment': 0
        }
    
    credit_score = calculate_credit_score(customer_id)
    
    # Check current EMI load
    current_loans = Loan.objects.filter(customer=customer, end_date__gte=date.today())
    current_emi = sum(loan.monthly_repayment for loan in current_loans)
    monthly_installment = calculate_monthly_installment(loan_amount, interest_rate, tenure)
    total_emi = current_emi + monthly_installment
    
    # 50% of monthly salary check
    max_allowed_emi = customer.monthly_salary * Decimal('0.5')
    if total_emi > max_allowed_emi:
        return {
            'customer_id': customer_id,
            'approval': False,
            'interest_rate': interest_rate,
            'corrected_interest_rate': interest_rate,
            'tenure': tenure,
            'monthly_installment': monthly_installment
        }
    
    # Determine approval and corrected interest rate based on credit score
    approval = False
    corrected_interest_rate = interest_rate
    
    if credit_score > 50:
        approval = True
    elif 30 < credit_score <= 50:
        approval = interest_rate > 12
        if approval and interest_rate <= 12:
            corrected_interest_rate = 12.01
    elif 10 < credit_score <= 30:
        approval = interest_rate > 16
        if approval and interest_rate <= 16:
            corrected_interest_rate = 16.01
    else:
        approval = False
    
    # Recalculate EMI with corrected interest rate
    if corrected_interest_rate != interest_rate:
        monthly_installment = calculate_monthly_installment(loan_amount, corrected_interest_rate, tenure)
    
    return {
        'customer_id': customer_id,
        'approval': approval,
        'interest_rate': interest_rate,
        'corrected_interest_rate': corrected_interest_rate,
        'tenure': tenure,
        'monthly_installment': monthly_installment
    }
