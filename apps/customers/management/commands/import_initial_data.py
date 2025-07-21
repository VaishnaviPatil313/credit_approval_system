from django.core.management.base import BaseCommand
from apps.customers.tasks import load_customer_data
from apps.loans.tasks import load_loan_data

class Command(BaseCommand):
    help = "Load initial customer and loan data asynchronously using Celery background tasks"

    def handle(self, *args, **options):
        load_customer_data.delay()
        load_loan_data.delay()
        self.stdout.write(
            self.style.SUCCESS(
                'Triggered background Celery tasks to load customer and loan data. Check Celery logs for progress.'
            )
        )

