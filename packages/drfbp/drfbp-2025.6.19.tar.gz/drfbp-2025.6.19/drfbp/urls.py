URLS = """
from django import urls
from rest_framework import routers

from {path} import views

router = routers.DefaultRouter()
router.register(r"", views.{model}ModelViewSet, basename="{appname}")

urlpatterns = [
    urls.path("", urls.include(router.urls)),
]
"""
