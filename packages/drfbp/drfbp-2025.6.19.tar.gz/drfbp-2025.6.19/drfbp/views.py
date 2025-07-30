VIEWS = """
from rest_framework import permissions, viewsets

from {app} import models
from {path}.permissions import {model}BasePermission
from {path}.serializers import {model}ModelSerializer


class {model}ModelViewSet(viewsets.ModelViewSet):
    queryset = models.{model}.objects.all()
    serializer_class = {model}ModelSerializer
    permission_classes = [permissions.IsAuthenticated, {model}BasePermission]
    http_method_names = ["get", "post", "put", "delete"]
    lookup_field = "id"

    def get_queryset(self):
        return super().get_queryset()
"""
