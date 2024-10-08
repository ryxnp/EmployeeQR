from django.contrib import admin
from django.urls import path,include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

admin.site.site_header = 'Employee Records'
admin.site.site_title = 'Employee Records'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('eqrApp.urls')),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls'))
]
