"""onspace URL Configuration

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
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from accounts.views import home, about


urlpatterns = [
    path('',home),
    path('about/', about),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('information/', include('information.urls')),
    path('news/', include('news.urls')),
    path('dealflowbox/', include('dealflowbox.urls')),
    path('project/', include('recommender.urls')),
    # path('accounts/', include('django.contrib.auth.urls')),
] 
# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += (static(settings.STATIC_URL, document_root=settings.STATIC_ROOT))