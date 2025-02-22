from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib import admin
from dotenv import load_dotenv
from . import views
from django.views.generic import RedirectView
from .views import CustomTokenObtainPairView, CustomTokenRefreshView

load_dotenv()

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
   path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # Authentication URLs
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/', include('djoser.urls.authtoken')),
    
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),

    # App-specific URLs
    path('', include('accounts.urls')),  # Example: /accounts/
    path('api/', include('shop.urls')),      # Example: /products/
    path('admin/', admin.site.urls),     # Admin URLs: /admin/
    # Debug view
    #  path("__debug__/", include("debug_toolbar.urls")),
    #  path('debug/', TemplateView.as_view(template_name='../frontend/index.html'), name='index'),
    #re_path(r'^.*$', TemplateView.as_view(template_name='index.html'), name='index'),
    path("", views.index, name="index"),
    # Catch-all URL pattern (redirect to index.html)
    re_path(r'^.*$', RedirectView.as_view(url='/')),


    # Default URL (index.html)
]

if settings.DEBUG:
    # Serve media files
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Serve static files collected in STATIC_ROOT after running collectstatic
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # Optionally, serve assets from the second directory in STATICFILES_DIRS
    urlpatterns += static('/assets/', document_root=settings.STATICFILES_DIRS[1])
    
 #   urlpatterns += static('/assets/', document_root=settings.STATICFILES_ROOT[1])




       
       
