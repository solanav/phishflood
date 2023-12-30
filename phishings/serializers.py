from django.contrib.auth.models import Group, User
from rest_framework import serializers
from .models import Phishing, Form, Input, Action


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "groups"]


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name"]


class PhishingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phishing
        fields = ["id", "url"]


class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        fields = [
            "phishing",
            "meta_id",
            "html_id",
            "html_action",
            "html_method",
            "html_type",
        ]


class InputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Input
        fields = [
            "form",
            "meta_id",
            "html_id",
            "html_name",
            "html_placeholder",
            "html_type",
        ]


class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = ["phishing", "action", "form", "input", "value", "status"]
