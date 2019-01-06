from django.urls import include, path, re_path
from rest_framework_swagger.views import get_swagger_view
from apps.api_rest import views

schema_view = get_swagger_view(title='API')

urlpatterns = [
    # AUTH
    path('', schema_view),
    path('login/', views.Login.as_view(), name="login"),
    path('register/', views.Register.as_view(), name="register"),
    path('rest-auth/facebook/', views.FacebookLogin.as_view(), name='fb_login'),
    path('convert_token/', views.ConvertToken.as_view(), name='convert_token'),

    path('cotacao/seguro/', views.CotarSeguro.as_view(), name="cotacao-seguro"),

]
