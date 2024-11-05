from django.contrib import admin
from django.urls import path, include, reverse_lazy
from users.forms import CustomUserCreationForm
from django.views.generic.edit import CreateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('auth/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('', include('aplication.urls')),
    path(
      'auth/registration/',
      CreateView.as_view(
          template_name='registration/registration_form.html',
          form_class=CustomUserCreationForm,
          success_url=reverse_lazy('aplication:index'),
      ),
      name='registration',
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
