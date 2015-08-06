from django.conf.urls import include, url
from django.contrib import admin
from consumption.api import RecordResource, RecordResource2, UserResource
from tastypie.api import Api

api = Api()
api.register(RecordResource())
api.register(UserResource())
api.register(RecordResource2())

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(api.urls)),
]
