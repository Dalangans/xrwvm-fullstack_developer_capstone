from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView, RedirectView # Tambahkan RedirectView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('djangoapp/', include('djangoapp.urls')),
    
    path('manifest.json', RedirectView.as_view(url='/static/manifest.json')),
    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico')),
    path('logo192.png', RedirectView.as_view(url='/static/logo192.png')),

    path('', TemplateView.as_view(template_name="Home.html")),
    path('about/', TemplateView.as_view(template_name="About.html")),
    path('contact/', TemplateView.as_view(template_name="Contact.html")),
    path('login/', TemplateView.as_view(template_name="index.html")),
    path('logout/', TemplateView.as_view(template_name="index.html")),
    path('register/', TemplateView.as_view(template_name="index.html")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)