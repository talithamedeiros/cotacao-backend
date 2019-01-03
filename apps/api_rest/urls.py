from django.conf.urls import url
from rest_framework_swagger.views import get_swagger_view
from apps.api_rest import views

schema_view = get_swagger_view(title='API')

urlpatterns = [
    url('^$', schema_view),
    url(r'^login/$', views.Login.as_view(), name="login"),
    url(r'^register/$', views.Register.as_view(), name="register"),
    url(r'^rest-auth/facebook/$', views.FacebookLogin.as_view(), name='fb_login'),
    url(r'^convert_token/$', views.ConvertToken.as_view(), name='convert_token'),
]
