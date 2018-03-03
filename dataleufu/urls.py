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
from places.views import PlaceViewSet, CategoryViewSet, PlacesListAPIView, LayerViewSet, PlaceDetailView
from .views import UserGroupViewSet, UserProfileViewSet, LoginView, UserViewSet, ResetPasswordView, \
    FacebookLoginView, FacebookSignupView, FacebookLogin
from rest_framework import routers


from django.conf import settings
from django.conf.urls.static import static
from votes import urls as votesUrls

router = routers.DefaultRouter()
router.register(r'api_places', PlaceViewSet)
router.register(r'api_categories', CategoryViewSet)
router.register(r'api_layers', LayerViewSet)
router.register(r'api_user_group', UserGroupViewSet)
router.register(r'api_user_profile', UserProfileViewSet)
#router.register(r'api_register', UserViewSet)
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^places/(?P<category_pk>.+)/$', PlacesListAPIView.as_view(), name='places'),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^map/(?P<pk>[-\w]+)/$', PlaceDetailView.as_view(), name='place'),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^rest-auth/facebook/$', FacebookLogin.as_view(), name='fb_login'),
    url(r'^accounts/', include('allauth.urls'), name='socialaccount_signup'),
    url(r'^', include('django.contrib.auth.urls')), #necesario para el password reset

    url(r'^', include(router.urls)),
    url(r'^api_login', LoginView.as_view(), name="api_login"),
    url(r'^', include(votesUrls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
