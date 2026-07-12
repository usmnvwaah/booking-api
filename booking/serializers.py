from rest_framework import serializers
from .models import Resource, Booking
from django.utils import timezone


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    resource_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'resource_id', 'resource', 'user', 'start', 'end', 'status']
        read_only_fields = ['resource', 'user', 'status']

    def validate(self, data):
        request = self.context['request']

        start = data['start']
        end = data['end']

        # 1. start < end
        if start >= end:
            raise serializers.ValidationError("start must be less than end")

        # 2. не в прошлом
        if start < timezone.now():
            raise serializers.ValidationError("Cannot book in the past")

        # 3. пересечение
        resource_id = data['resource_id']

        qs = Booking.objects.filter(
            resource_id=resource_id,
            status='active',
            start__lt=end,
            end__gt=start
        )

        if qs.exists():
            raise serializers.ValidationError("Ресурс уже забронирован на это время.")

        return data

    def create(self, validated_data):
        request = self.context['request']

        resource_id = validated_data.pop('resource_id')

        return Booking.objects.create(
            resource_id=resource_id,
            user=request.user,
            **validated_data
        )