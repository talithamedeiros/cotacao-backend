"""projeto URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.views import defaults as default_views
from django.views.generic import RedirectView

admin.site.site_header = settings.ADMIN_SITE_HEADER

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='auth-login', permanent=False)),

    # ADMIN
    # path('admin/', include('smuggler.urls')),
    # path('grappadminelli/', include('grappelli.urls')), # grappelli URLS
    path('admin/', admin.site.urls),
    path('admin/doc/', include('django.contrib.admindocs.urls')),

    # I18N
    # path('i18n/', include('django.conf.urls.i18n')),

    # API
    path('api/', include('apps.api_rest.urls')),
	path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # AUTH
    # path('accounts/', include('allauth.urls')),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    
    # CUSTOM
    path('default/', include('apps.default.urls')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)