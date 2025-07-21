from django.db import connection
import pandas as pd
from celery import shared_task
from .models import Customer
from apps.loans.models import Loan


@shared_task
def load_customer_data():
    """Safely load customer data after ensuring table exists."""
    try:
        # Check if table exists
        if 'customers_customer' not in connection.introspection.table_names():
            return "Customer table does not exist. Run migrations first."

        df = pd.read_excel('/app/data/customer_data.xlsx')

        for _, row in df.iterrows():
            Customer.objects.update_or_create(
                customer_id=row['Customer ID'],
                defaults={
                    'first_name': row['First Name'],
                    'last_name': row['Last Name'],
                    'age': row['Age'],
                    'phone_number': str(row['Phone Number']),
                    'monthly_salary': row['Monthly Salary'],
                    'approved_limit': row['Approved Limit'],
                    'current_debt': 0
                }
            )

        return f"Successfully loaded {len(df)} customers"

    except Exception as e:
        return f"Error loading customer data: {str(e)}"



@shared_task
def load_loan_data():
    """Import loans from the formatted Excel file."""
    try:
        df = pd.read_excel('/app/data/loan_data.xlsx')

        for _, row in df.iterrows():
            try:
                customer = Customer.objects.get(customer_id=row['Customer ID'])
                start_date = pd.to_datetime(row['Date of Approval']).date()
                end_date = pd.to_datetime(row['End Date']).date()
                Loan.objects.update_or_create(
                    loan_id=row['Loan ID'],
                    defaults={
                        'customer': customer,
                        'loan_amount': row['Loan Amount'],
                        'tenure': row['Tenure'],
                        'interest_rate': row['Interest Rate'],
                        'monthly_repayment': row['Monthly payment'],
                        'emis_paid_on_time': row['EMIs paid on Time'],
                        'start_date': start_date,
                        'end_date': end_date
                    }
                )
            except Customer.DoesNotExist:
                continue

        return f"Successfully loaded {len(df)} loans"
    except Exception as e:
        return f"Error loading loan data: {str(e)}"


