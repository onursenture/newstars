from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'newstars.views.home', name='home'),
    # url(r'^newstars/', include('newstars.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    (r'^$', 'newstars.nws.views.home'),

    (r'^index/$', 'newstars.nws.views.home'),
    
    (r'^index/register/$', 'newstars.nws.views.register'),
    
    (r'^index/transcript/$', 'newstars.nws.views.transcript'),
    
    (r'^index/course/(?P<code>.*)/(?P<secID>.*)/$', 'newstars.nws.views.course_inst'),
    
    (r'^index/put:(?P<type>.*)/$', 'newstars.nws.views.add_element'),
    
    (r'^index/course/(?P<code>.*)/$', 'newstars.nws.views.course'),
    
    (r'^index/section/remap/(?P<s_id>.*)/$', 'newstars.nws.views.get_sec_data'),
    
    (r'^index/section/getmap/$', 'newstars.nws.views.get_all_secs'),
    
    (r'^index/section/add/(?P<s_id>.*)/$', 'newstars.nws.views.add_section'),
    
    (r'^index/section/drop/(?P<s_id>.*)/$', 'newstars.nws.views.drop_section'),
    
    (r'^index/read:(?P<type>.*)/(?P<id>.*)/$', 'newstars.nws.views.read_element'),
    
    (r'^index/login/$', 'newstars.nws.views.login_screen'),
    
    (r'^accounts/login/$', 'newstars.nws.views.login_screen'),
    
    (r'^index/log/$', 'newstars.nws.views.login'),
    
    (r'^index/logout/$', 'newstars.nws.views.logout'),
    
    (r'^index/js/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/gma/www/newstars/public/templates/js/'}),
    
    (r'^index/css/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/gma/www/newstars/public/templates/css/'}),
    
    (r'^index/img/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/gma/www/newstars/public/templates/img/'})
)
