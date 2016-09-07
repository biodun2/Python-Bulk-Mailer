from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
admin.autodiscover()
from bulkmime.mails.views import home
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bulkmime.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', home),
    url(r'^admin/', include(admin.site.urls)),
)+ static('/media/', document_root='/home/bulkmime/bulkmime/media')
