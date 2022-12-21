from django.db.models import Avg
from rest_framework import serializers

from applications.feedback.models import Like, Rating
from applications.product.models import Category, Product, Image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    @staticmethod
    def validate_title(title):
        if Category.objects.filter(title=title.lower()).exists:
            raise serializers.ValidationError('Такое название уже существует!')
        return title


class ProductSerializer(serializers.ModelSerializer):
    images = ImageSerializer(required=False, many=True)
    # owner = serializers.ReadOnlyField(source='owner.email')
    owner = serializers.EmailField(required=False)

    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        product = Product.objects.create(**validated_data)
        request = self.context.get('request')
        user = request.user
        files = request.FILES
        list_images = []
        for image in files.getlist('images'):
            list_images.append(Image(image=image, product=product, owner=user))
        Image.objects.bulk_create(list_images)
        return product

    def update(self, instance, validated_data):
        request = self.context.get('request')
        user = request.user
        files = request.FILES
        image_list = []
        for image in files.getlist('images'):
            image_list.append(Image(image=image, product=instance, owner=user))
        Image.objects.bulk_create(image_list)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        images = []
        for image in rep['images']:
            images.append(image['image'])
        rep['images'] = images
        request = self.context.get('request')
        rep['likes'] = Like.objects.filter(
            owner=request.user,
            product=instance,
            like=True
        ).count()
        rep['rating'] = Rating.objects.filter(
            owner=request.user,
            product=instance
        ).aggregate(Avg('rating'))['rating__avg']
        if not rep['rating']:
            rep['rating'] = 0
        return rep

