from django.conf.urls import url
from django.contrib import admin
from jasset import views

urlpatterns = [
    url(r'asset$', views.asset_list, name="asset_list"),
    url(r'api$', views.asset_api, name="asset_api"),
    url(r'host$', views.host_list, name="host_list"),
    url(r'assetinfo/(?P<asset_id>\d+)$', views.asset_info, name="asset_info"),
    url(r'assetrecord$', views.assetrecord_list, name="assetrecord_list"),
    url(r'asseterrorlog$', views.asseterrorlog_list, name="asseterrorlog_list"),
]
