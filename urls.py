from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    # (r'^sebastian/', include('sebastian.foo.urls')),

     (r'^$', 'sebastian.leitner.views.index'),
     (r'^admin/', include('django.contrib.admin.urls')),
)
