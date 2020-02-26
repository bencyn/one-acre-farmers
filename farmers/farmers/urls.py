"""farmers URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path , include
from api import url ,views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'customers',views.CustomerViewSet)
router.register(r'seasons',views.SeasonsViewSet)
router.register(r'customerSummaries',views.CustomerSummariesView)
router.register(r'repayments',views.RepaymentsView)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('repaymentUploads', views.RepaymentUploadsView.as_view())
   
]


