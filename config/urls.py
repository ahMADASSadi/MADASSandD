from django.conf.urls.i18n import i18n_patterns
from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path("madassandd-admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
]

urlpatterns += i18n_patterns(
    path("", include("app.urls")),
)
