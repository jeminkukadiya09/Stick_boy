from django.contrib import admin
from django.urls import path,include



urlpatterns = [
    path('', include('application.urls')),


    path('admin/', admin.site.urls),
    path('', include('django.contrib.auth.urls')),
    
   ]
