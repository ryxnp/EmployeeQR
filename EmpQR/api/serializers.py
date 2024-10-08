from rest_framework import serializers
from eqrApp.models import Employee, LogRecord


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

class LogRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogRecord
        fields = '__all__'