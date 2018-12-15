from django.conf.urls import url
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^result/$', views.result, name='result'),
    url(r'^result_detail/(?P<query>\d+)/$', views.result_detail, name='result_detail'),
]
urlpatterns += static('media', document_root=settings.MEDIA_ROOT)