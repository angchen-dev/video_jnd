"""videoJnd URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from videoJnd import views 
from django.views import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.home, name="home"),
    path("eyetracking_jnd/", views.etjnd, name="etjnd"),
    path("scheduler", views.scheduler, name="scheduler"),
    url(r'^static/(?P<path>.*)$', static.serve,{'document_root': settings.STATIC_ROOT}, name='static'),
]

# handler400 = "videoJnd.views.error_test_400"
# handler403 = "videoJnd.views.error_test_403"
# handler404 = "videoJnd.views.error_test_404"
# handler500 = "videoJnd.views.error_test_500"