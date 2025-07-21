from django.db import models
from apps.customers.models import Customer

class Loan(models.Model):
    loan_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='loans')
    loan_amount = models.DecimalField(max_digits=15, decimal_places=2)
    tenure = models.IntegerField()  # in months
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    monthly_repayment = models.DecimalField(max_digits=12, decimal_places=2)
    emis_paid_on_time = models.IntegerField(default=0)
    start_date = models.DateField()
    end_date = models.DateField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Loan {self.loan_id} - {self.customer.first_name} {self.customer.last_name}"
    
    @property
    def repayments_left(self):
        from datetime import date
        from dateutil.relativedelta import relativedelta
        
        current_date = date.today()
        if current_date >= self.end_date:
            return 0
        
        months_passed = (current_date.year - self.start_date.year) * 12 + (current_date.month - self.start_date.month)
        return max(0, self.tenure - months_passed)
