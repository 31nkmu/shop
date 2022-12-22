from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from applications.order.models import Order
from applications.order.serializers import OrderSerializer


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(owner=self.request.user)


class OrderConfirmApiView(APIView):
    @staticmethod
    def get(request, activation_code):
        order = get_object_or_404(Order, activation_code=activation_code)
        if not order.is_confirm:
            order.status = 'in_processing'
            order.is_confirm = True
            order.save(update_fields=['is_confirm', 'status'])
            return Response({'msg': 'Заказ успешно подтвержден'}, status=status.HTTP_200_OK)
        return Response({'msg': 'Вы уже подтвердили заказ'}, status=status.HTTP_400_BAD_REQUEST)
