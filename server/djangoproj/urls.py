from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView, RedirectView # Tambahkan RedirectView
from django.conf.urls.static import static
from django.conf import settings
from djangoapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('djangoapp/', include('djangoapp.urls')),
    
    # API endpoints (aliases for frontend compatibility)
    path('api/fetchDealers', views.get_dealerships, name='api_fetchDealers'),
    path('api/fetchDealers/<str:state>', views.get_dealerships, name='api_fetchDealers_by_state'),
    path('api/fetchDealer/<int:dealer_id>', views.get_dealer_details, name='api_fetchDealer'),
    path('api/fetchReviews/dealer/<int:dealer_id>', views.get_dealer_reviews, name='api_fetchReviews'),
    path('api/addReview', views.add_review, name='api_addReview'),
    
    path('manifest.json', RedirectView.as_view(url='/static/manifest.json')),
    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico')),
    path('logo192.png', RedirectView.as_view(url='/static/logo192.png')),

    path('', TemplateView.as_view(template_name="Home.html")),
    path('about/', TemplateView.as_view(template_name="About.html")),
    path('contact/', TemplateView.as_view(template_name="Contact.html")),
    path('login/', TemplateView.as_view(template_name="index.html")),
    path('logout/', TemplateView.as_view(template_name="index.html")),
    path('register/', TemplateView.as_view(template_name="index.html")),
    path('dealers/', TemplateView.as_view(template_name="index.html")),
    path('dealer/<int:dealer_id>', TemplateView.as_view(template_name="index.html")),
    path('postreview/<int:dealer_id>', TemplateView.as_view(template_name="index.html")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)