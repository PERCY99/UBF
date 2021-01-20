
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework import routers
import rest_framework
from core.views import FacebookLogin
router = routers.DefaultRouter()



urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),

    path('rest-auth/facebook/', FacebookLogin.as_view(), name='fb_login'),

    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('nested_admin', include('nested_admin.urls')),
    path('api/core/', include('core.urls', namespace='core')),
    path('api/blog/', include('blog.urls', namespace='blog')),
    path('api/quiz/', include('quiz.urls', namespace='quiz')),
    path('api/cart/', include('cart.urls', namespace='cart')),
]

urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)