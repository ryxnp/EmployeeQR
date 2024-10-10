from rest_framework import serializers
from eqrApp.models import Employee, LogRecord
from rest_framework import viewsets


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

class LogRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogRecord
        fields = '__all__'

class LogRecordViewSet(viewsets.ModelViewSet):
    serializer_class = LogRecordSerializer

    def get_queryset(self):
        queryset = LogRecord.objects.all()
        employee_id = self.request.query_params.get('employee_id', None)
        if employee_id is not None:
            queryset = queryset.filter(employee_pk=employee_id)  # Adjust field name as necessary
        return queryset