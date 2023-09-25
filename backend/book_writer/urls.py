from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from sections import views as section_views

router = routers.DefaultRouter()
router.register(r'sections', section_views.SectionViewSet, basename='section')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('register/', section_views.UserRegistrationView.as_view(), name='register'),
    path('login/', section_views.UserLoginView.as_view(), name='login'),
]


