from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView 
from posts.views import ValidateTokenView, GoogleLogin, CustomTokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('posts/', include('posts.urls')), # posts app url
    path('accounts/', include('allauth.urls')),  # For Google OAuth callbacks
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
    path('api/auth/social/google/', GoogleLogin.as_view(), name='google_login'),  # Handles Google login/token exchange

    path('api/validate-token/', ValidateTokenView.as_view(), name='validate-token'),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/', include('djoser.urls.jwt')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

