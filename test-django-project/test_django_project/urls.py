from django.urls import include, path


urlpatterns = [
    path("", include("testapp.urls", namespace="testapp")),
]
