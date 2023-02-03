from django.urls import path
from . import views
from .views import MyTokenObtainPairView

from rest_framework_simplejwt.views import (
    TokenRefreshView
)
from django.conf import settings


urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('',views.testRoute),
    path('parishes/',views.getParishes),
    path('counties/',views.getCounties),
    path('cleanse/',views.cleanse),
    path('upload/',views.upload),
    path('points/',views.getPoints),
    path('reverse/',views.reverseGeocode),
    path('cleansefile/',views.cleanseUpload)
]