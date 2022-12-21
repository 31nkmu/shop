from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from applications.feedback.models import Like, Rating
from applications.feedback.serializers import RatingSerializer
from applications.product.models import Product, Category
from applications.product.serializers import ProductSerializer, CategorySerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = ['category']
    search_fields = ['title']
    ordering_fields = ['price']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['POST'])
    def like(self, request, pk=None):
        like_obj, is_created = Like.objects.get_or_create(
            owner=request.user,
            product=self.get_object()
        )
        like_obj.like = not like_obj.like
        like_obj.save()
        status_ = 'Лайк убран'
        print(like_obj.like)
        if like_obj.like:
            status_ = 'Лайк добавлен'
        return Response({'status': status_}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'])
    def rating(self, request, pk=None):
        serializer = RatingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        rating_obj, is_created = Rating.objects.get_or_create(
            owner=request.user,
            product=self.get_object()
        )
        rating_obj.rating = request.data['rating']
        rating_obj.save()
        return Response(request.data, status=status.HTTP_201_CREATED)


class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
