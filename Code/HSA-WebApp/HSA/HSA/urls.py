"""HSA URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""


from django.conf.urls import url
from django.contrib import admin


from hsaApp import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^home', views.home, name='home'),
    url(r'^Monitoring', views.Monitoring, name='Monitoring'),
    url(r'^capimgrecvid', views.capimgrecvid, name='capimgrecvid'),
    url(r'^capimg', views.capimg, name='capimg'),
    url(r'^recvid', views.recvid, name='recvid'),
    url(r'^videorecorded', views.videorecorded, name='videorecorded'),
    
    
    url(r'^turnOn', views.turnOn, name='turnOn'),
    url(r'^turnOff', views.turnOff, name='turnOff'),
    
]
