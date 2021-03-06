"""store URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls import url


urlpatterns = [
    path('admin/', admin.site.urls),
    url('api/base/', include(('base.urls', 'base'), namespace='base')),
    url('api/store_in/', include(('storein.urls', 'base'), namespace='store_in')),
    url('api/purchase/', include(('purchase.urls', 'base'), namespace='purchase')),
    url('api/purchaseRequest/', include(('purchaseRequest.urls', 'base'), namespace='purchaseRequest')),
    # url('api/warehousing/', include(('warehousing.urls', 'base'), namespace='warehousing')),
    url('api/store_manage/', include(('storeManage.urls', 'base'), namespace='store_manage')),
    url('api/store_adjust/', include(('storeAdjust.urls', 'base'), namespace='store_adjust')),
]
