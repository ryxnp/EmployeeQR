from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet, LogRecordViewSet

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)
router.register(r'logrecords', LogRecordViewSet)  # Add this line

urlpatterns = [
    path('', include(router.urls)),
]