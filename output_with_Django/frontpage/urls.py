from django.conf.urls import url
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.index, name='index'),
    #url(r'^result/$', views.result, name='result'),
]
urlpatterns += static('media', document_root=settings.MEDIA_ROOT)