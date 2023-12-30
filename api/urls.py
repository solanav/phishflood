from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from phishings import views

router = routers.DefaultRouter()

router.register(r"api/v1/users", views.UserViewSet)
router.register(r"api/v1/groups", views.GroupViewSet)

router.register(
    r"api/v1/fullphishing", views.FullPhishingViewSet, basename="fullphishing"
)
router.register(r"api/v1/phishing", views.PhishingViewSet)
router.register(r"api/v1/form", views.FormViewSet)
router.register(r"api/v1/input", views.InputViewSet)
router.register(r"api/v1/action", views.ActionViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("", include(router.urls)),
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]

urlpatterns += router.urls
