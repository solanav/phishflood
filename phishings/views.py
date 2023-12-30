import json
import pika
from config import rabbit_conf
from typing import Dict
from phishings.models import Phishing, Form, Input, Action
from rest_framework import viewsets
from django.contrib.auth.models import User, Group
from rest_framework import permissions
from rest_framework.response import Response
from pika.exchange_type import ExchangeType
from phishings.serializers import (
    GroupSerializer,
    UserSerializer,
    PhishingSerializer,
    FormSerializer,
    InputSerializer,
    ActionSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class FullPhishingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that returns all phishings as a single object with nested forms, inputs, and actions.
    """

    queryset = Phishing.objects.all()
    serializer_class = PhishingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def fullphishing(self, request, id: str) -> Dict:
        phishing = Phishing.objects.get(id=id)

        json_phishing = self.get_serializer(phishing).data
        json_phishing["forms"] = []
        json_phishing["actions"] = []

        forms = Form.objects.filter(phishing=phishing)
        for form in forms:
            json_form = FormSerializer(form, context={"request": request}).data
            assert isinstance(json_form, Dict)

            json_form["inputs"] = []

            inputs = Input.objects.filter(form=form)
            for input_obj in inputs:
                json_input = InputSerializer(
                    input_obj, context={"request": request}
                ).data
                json_form["inputs"].append(json_input)

            json_phishing["forms"].append(json_form)

        actions = Action.objects.filter(phishing=phishing)
        for action in actions:
            json_action = ActionSerializer(action, context={"request": request}).data
            json_phishing["actions"].append(json_action)

        return json_phishing

    def retrieve(self, request, pk: str):
        return Response(self.fullphishing(request, pk))

    def list(self, request, *args, **kwargs):
        return Response(
            [
                self.fullphishing(request, phishing.id)
                for phishing in self.get_queryset()
            ]
        )


class PhishingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows phishings to be viewed or edited.
    """

    queryset = Phishing.objects.all()
    serializer_class = PhishingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        print("Saving object to database")
        instance = serializer.save()
        instance.save()
        print(f"Saved {instance.url} to database")

        # Create the JSON to send to the rabbitmq queue
        body = json.dumps({"url": instance.url})

        # Send the URL to the rabbitmq queue
        print(f"Publishing message to rabbitmq for {instance.url}")
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=rabbit_conf.HOST)
        )
        channel = connection.channel()
        channel.queue_declare(queue=rabbit_conf.QUEUE)
        channel.exchange_declare(exchange=rabbit_conf.EXCHANGE, exchange_type="topic")
        channel.basic_publish(
            exchange=rabbit_conf.EXCHANGE, routing_key=rabbit_conf.QUEUE, body=body
        )
        connection.close()


class FormViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows forms to be viewed or edited.
    """

    queryset = Form.objects.all()
    serializer_class = FormSerializer
    permission_classes = [permissions.IsAuthenticated]


class InputViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows inputs to be viewed or edited.
    """

    queryset = Input.objects.all()
    serializer_class = InputSerializer
    permission_classes = [permissions.IsAuthenticated]


class ActionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows actions to be viewed or edited.
    """

    queryset = Action.objects.all()
    serializer_class = ActionSerializer
    permission_classes = [permissions.IsAuthenticated]
