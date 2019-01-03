#-*- coding: utf-8 -*-

##################################################
#				DJANGO IMPORTS                   #
##################################################
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.contrib import admin
from django.core.urlresolvers import reverse_lazy
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib.auth.decorators import login_required
##################################################


'''
	DJANGO URLS
'''

urlpatterns = [
	url(r'^admin/', include('smuggler.urls')), 
    url(r'^admin/', admin.site.urls),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
	url(r'^api_rest/', include('apps.api_rest.urls')),
	url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += (
       url(r'^__debug__/', include(debug_toolbar.urls)),
    )

'''
	CUSTOM URLS
'''
urlpatterns += (
	url(r'^$', RedirectView.as_view(url=reverse_lazy('login'))),
	url(r'^framework/', include('apps.default.urls')),
)


'''
	MEDIA
'''
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


'''
    DJANGO-FILER
'''

urlpatterns += [
    url(r'^filer/', include('filer.urls')),
]