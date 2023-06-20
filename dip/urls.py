"""Diplom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from api.views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

router = routers.DefaultRouter()

router.register(r'models', AllModelView, basename='model1')
router.register(r'generations', AllGenView, basename='model2')
router.register(r'engines', AllEngineView, basename='model3')
router.register(r'params', AllParamsView, basename='model4')


urlpatterns = [
    path('', include(router.urls)),

    path('admin/', admin.site.urls),

    path('api/v1/recognition/', RecognitionView.as_view()),

    path('api/v1/company/', CompanyView.as_view()),
    path('api/v1/company/detail=<int:pk>', CompanyViewDetail.as_view()),
    path('api/v1/company/<int:name>/', ModelView.as_view()),
    path('api/v1/company/<int:name>/detail=<int:pk>', ModelViewDetail.as_view()),
    path('api/v1/company/<int:name>/<int:gen>/', GenerationView.as_view()),
    path('api/v1/company/<int:name>/<int:gen>/detail=<int:pk>', GenerationViewDetail.as_view()),
    path('api/v1/company/<int:name>/<int:gen>/<int:eng>/', EngineView.as_view()),
    path('api/v1/company/<int:name>/<int:gen>/<int:eng>/detail=<int:pk>', EngineViewDetail.as_view()),
    path('api/v1/company/<int:name>/<int:gen>/<int:eng>/<int:eng_par>/', EngineParamsView.as_view()),

    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),   # проверка токена на валидность
]
