SERIALIZERS = """
from rest_framework import serializers

from {app} import models


class {model}ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.{model}
        exclude = []
        read_only_fields = []
"""
