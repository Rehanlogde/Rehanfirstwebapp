from . import views
from django.contrib import admin
from django.urls import path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('verifying', views.verify),
    path('mainhomepage' , views.userhome),
    path('registration', views.register),
    path('registrationresult', views.registrationresult),
    path('logout', views.loggingout),
    path('mfapinrecovery', views.mfarecovery),
    path('customization', views.customize),
    path('result', views.result),
    path('404', views.invalidwebpage)
]
