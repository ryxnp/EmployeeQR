from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import EmployeeSerializer, LogRecordSerializer
from django.http import Http404
from rest_framework import viewsets
from eqrApp.models import LogRecord, Employee

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()  # Define your queryset here
    serializer_class = EmployeeSerializer

class LogRecordViewSet(viewsets.ModelViewSet):
    queryset = LogRecord.objects.all()
    serializer_class = LogRecordSerializer

class EmployeeList(APIView):
    def get(self, request, format=None):
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmployeeDetail(APIView):
    def get_object(self, pk):
        try:
            return Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        employee = self.get_object(pk)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        employee = self.get_object(pk)
        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        employee = self.get_object(pk)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class LogRecordList(APIView):
    def get(self, request, format=None):
        log_records = LogRecord.objects.all()
        serializer = LogRecordSerializer(log_records, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = LogRecordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogRecordDetail(APIView):
    def get_object(self, pk):
        try:
            return LogRecord.objects.get(pk=pk)
        except LogRecord.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        log_record = self.get_object(pk)
        serializer = LogRecordSerializer(log_record)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        log_record = self.get_object(pk)
        serializer = LogRecordSerializer(log_record, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        log_record = self.get_object(pk)
        log_record.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)