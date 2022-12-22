from rest_framework import serializers

from applications.order.models import Order
from applications.order.send_mail import send_activation_link


class OrderSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Order
        exclude = ['activation_code']

    def create(self, validated_data):
        amount = validated_data['amount']
        product = validated_data['product']
        if amount > product.amount:
            raise serializers.ValidationError(f'Нет такого количества! Осталось {product.amount}')
        if amount == 0:
            raise serializers.ValidationError('Минимум один товар')
        product.amount -= amount
        product.save(update_fields=['amount'])
        request = self.context.get('request')
        order = Order.objects.create(**validated_data)
        send_activation_link(email=request.user.email, activation_code=order.activation_code, title=order.product,
                             price=order.total_price)
        return order
