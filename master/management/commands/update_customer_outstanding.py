import pandas as pd
from django.db import transaction
from accounts.models import CustomUser, Customers
from client_management.models import CustomerOutstanding, OutstandingAmount, CustomerOutstandingReport

# Read the Excel file
file_path = '/home/ra/Downloads/outstanding_update.xlsx'
data = pd.read_excel(file_path)
print("File path:", file_path)
print("DataFrame columns:", data.columns)

# Strip any leading/trailing whitespace from column names
data.columns = data.columns.str.strip()
print("Stripped DataFrame columns:", data.columns)

# Verify that 'amount' column exists
if 'amount' not in data.columns:
    raise KeyError("Column 'amount' not found in the DataFrame. Available columns: " + ", ".join(data.columns))

# Assuming the excel columns are named as follows:
# 'customer_name', 'product_type', 'amount', 'created_by', 'modified_by'

@transaction.atomic
def populate_models_from_excel(data):
    user = CustomUser.objects.get(username="SW-40")
    for index, row in data.iterrows():
        customer_name = row['customer_name']
        amount = row['amount']

        # Get or create customer
        try:
            customer = Customers.objects.get(customer_name=customer_name)
        except Customers.DoesNotExist:
            print(f"Customer {customer_name} does not exist.")
            continue

        # Get or create CustomerOutstanding
        customer_outstanding, created = CustomerOutstanding.objects.get_or_create(
            customer=customer,
            product_type='amount',
            defaults={
                'created_by': user.id,
                'modified_by': user.id,
            }
        )

        if not created:
            # Update modified_by and modified_date if it already exists
            customer_outstanding.modified_by = user.id
            customer_outstanding.save()

        # Create OutstandingAmount
        outstanding_amount = OutstandingAmount.objects.create(
            customer_outstanding=customer_outstanding,
            amount=amount
        )

        # Update or create CustomerOutstandingReport
        report, created = CustomerOutstandingReport.objects.update_or_create(
            customer=customer,
            product_type='amount',
            defaults={'value': amount}
        )

        if not created:
            # If the report already exists, add the new amount to the existing value
            report.value += amount
            report.save()

        print(f"Processed row {index + 1} for customer {customer_name}")

# Execute the function
populate_models_from_excel(data)
