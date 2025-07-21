from rest_framework import serializers
from .models import Customer

class CustomerRegistrationSerializer(serializers.ModelSerializer):
    monthly_income = serializers.DecimalField(max_digits=12, decimal_places=2, write_only=True)
    
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'age', 'phone_number', 'monthly_income']
    
    def create(self, validated_data):
        monthly_income = validated_data.pop('monthly_income')
        validated_data['monthly_salary'] = monthly_income
        
        # Calculate approved limit: 36 * monthly_salary (rounded to nearest lakh)
        approved_limit = round((36 * monthly_income) / 100000) * 100000
        validated_data['approved_limit'] = approved_limit
        
        return Customer.objects.create(**validated_data)

class CustomerResponseSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    monthly_income = serializers.DecimalField(source='monthly_salary', max_digits=12, decimal_places=2)
    
    class Meta:
        model = Customer
        fields = ['customer_id', 'name', 'age', 'monthly_income', 'approved_limit', 'phone_number']
    
    def get_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
