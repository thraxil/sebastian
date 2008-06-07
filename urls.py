from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    # (r'^sebastian/', include('sebastian.foo.urls')),

     (r'^$', 'sebastian.leitner.views.index'),
     (r'^add_card/$', 'sebastian.leitner.views.add_card'),
     (r'^test/$', 'sebastian.leitner.views.test'),
     (r'^stats/$', 'sebastian.leitner.views.stats'),
     (r'^admin/', include('django.contrib.admin.urls')),
)
