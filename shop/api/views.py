from datetime import timezone

from models import Category, Product
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveDestroyAPIView,
    RetrieveUpdateAPIView,
    get_object_or_404,
)
from serializer import (
    CategoryCreateUpdateSerializer,
    CategoryListSerializer,
    ProductListSerializer,
    ProductUpdateCreateSerializer,
)


class CategoryListAPI(ListAPIView):
    serializer_class = CategoryListSerializer

    def get_queryset(self):
        return Category.objects.filter(is_active=True)  # (user=self.request.user)

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(
            queryset,
        )
        return obj


class CategoryCreateAPI(CreateAPIView):
    serializer_class = CategoryCreateUpdateSerializer
    queryset = Category.objects.all()

    # def perform_create(self, serializer):
    #     return serializer.save(user=self.request.user)


class CategoryUpdateAPI(RetrieveUpdateAPIView):
    serializer_class = CategoryCreateUpdateSerializer
    queryset = Category.objects.all()
    lookup_field = "pk"
