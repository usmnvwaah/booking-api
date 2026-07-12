from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Resource, Booking
from .serializers import ResourceSerializer, BookingSerializer
from django.utils import timezone


class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.filter(is_active=True)
    serializer_class = ResourceSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [IsAdminUser()]
        return []


class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        booking = self.get_object()

        if booking.user != request.user:
            return Response({"detail": "Forbidden"}, status=403)

        if booking.status == 'cancelled':
            return Response({"detail": "Already cancelled"}, status=400)

        if booking.start <= timezone.now():
            return Response({"detail": "Too late to cancel"}, status=400)

        booking.status = 'cancelled'
        booking.save()

        return Response({"detail": "cancelled"})

# Create your views here.
