from dataclasses import fields
from pyexpat import model
from rest_framework import serializers
from buses.models import Bus


class BusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bus
        fields = [
            "id",
            "number",
            "seats",
            "start",
            "plate_number",
            "destination",
            "fee",
        ]


class BusAllocationSerializer(serializers.Serializer):

    id = serializers.IntegerField()

    def validate(self, attrs):

        try:
            bus = Bus.objects.get(pk=attrs.get("id"))
            attrs["bus"] = bus
        except Bus.DoesNotExist:
            raise serializers.ValidationError("Bus not found.")

        return attrs
