from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView # Import the TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    # This line serves your new index.html file at the home page ('')
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
]