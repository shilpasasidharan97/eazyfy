from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('official/',include('official.urls')),
    path('franchise/',include('franchise.urls')),
    path('pickupboy/',include('pickupboy.urls')),
    path('/',include('user.urls')),


]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
