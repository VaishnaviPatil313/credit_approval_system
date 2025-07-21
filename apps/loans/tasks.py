from celery import shared_task
import pandas as pd
from datetime import datetime
from .models import Loan
from apps.customers.models import Customer

@shared_task
def load_loan_data():
    """
    Load loan data from Excel file located at /app/data/loan_data.xlsx.
    """
    try:
        df = pd.read_excel('/app/data/loan_data.xlsx')
        for _, row in df.iterrows():
            try:
                customer = Customer.objects.get(customer_id=row['customer_id'])

                # Parse date columns safely
                start_date = pd.to_datetime(row['start_date']).date()
                end_date = pd.to_datetime(row['end_date']).date()
                
                Loan.objects.update_or_create(
                    loan_id=row['loan_id'],
                    defaults={
                        'customer': customer,
                        'loan_amount': row['loan_amount'],
                        'tenure': row['tenure'],
                        'interest_rate': row['interest_rate'],
                        'monthly_repayment': row['monthly_repayment'],
                        'emis_paid_on_time': row['EMIs_paid_on_time'],
                        'start_date': start_date,
                        'end_date': end_date
                    }
                )
            except Customer.DoesNotExist:
                continue

        return f"Successfully loaded {len(df)} loans"

    except Exception as e:
        return f"Error loading loan data: {str(e)}"

