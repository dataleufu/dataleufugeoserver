"""dataleufu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib.gis import admin
from places.views import PlaceViewSet, CategoryViewSet, PlacesListAPIView, LayerViewSet
from .views import UserGroupViewSet, UserProfileViewSet, LoginView, UserViewSet, ResetPasswordView, \
    FacebookLoginView, FacebookSignupView
from rest_framework import routers


from django.conf import settings
from django.conf.urls.static import static


router = routers.DefaultRouter()
router.register(r'api_places', PlaceViewSet)
router.register(r'api_categories', CategoryViewSet)
router.register(r'api_layers', LayerViewSet)
router.register(r'api_user_group', UserGroupViewSet)
router.register(r'api_user_profile', UserProfileViewSet)
router.register(r'api_register', UserViewSet)
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^places/(?P<category_pk>.+)/$', PlacesListAPIView.as_view(), name='places'),


    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api_login', LoginView.as_view(), name="api_login"),
    url(r'^api/reset-password', ResetPasswordView.as_view(), name="reset-password"),
    url(r'^api/sociallogin/login/facebook', FacebookLoginView.as_view(), name="facebook-login"),
    url(r'^api/sociallogin/signup/facebook', FacebookSignupView.as_view(), name="facebook-signup"),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
