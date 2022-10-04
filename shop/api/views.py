from datetime import timezone

from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    RetrieveDestroyAPIView,
    RetrieveUpdateAPIView,
    get_object_or_404,
)

from shop.api.serializer import (
    CategoryCreateUpdateSerializer,
    CategoryListSerializer,
    ProductListSerializer,
    ProductUpdateCreateSerializer,
)
from shop.models import Category, Product


class CategoryListAPI(ListAPIView):
    serializer_class = CategoryListSerializer

    def get_queryset(self):
        return Category.objects.filter(is_active=True)  # (user=self.request.user)

    # def get_object(self):
    #     queryset = self.get_queryset()
    #     obj = get_object_or_404(
    #         queryset,
    #     )
    #     return obj


class CategoryCreateAPI(CreateAPIView):
    serializer_class = CategoryCreateUpdateSerializer
    queryset = Category.objects.all()

    # def perform_create(self, serializer):
    #     return serializer.save(user=self.request.user)


class CategoryUpdateAPI(RetrieveUpdateAPIView):
    serializer_class = CategoryCreateUpdateSerializer
    queryset = Category.objects.all()
    lookup_field = "pk"


class CategoryDestroyAPI(RetrieveDestroyAPIView):
    serializer_class = CategoryListSerializer
    queryset = Category.objects.all()
    lookup_field = "pk"

    # def get_queryset(self):
    #     return Category.objects.filter(is_active=False)


class ProductListAPI(ListAPIView):
    serializer_class = ProductListSerializer

    def get_queryset(self):
        return Product.objects.filter(is_active=True)


class ProductCreateAPI(CreateAPIView):
    serializer_class = ProductUpdateCreateSerializer
    queryset = Product.objects.all()


class ProductDetailAPI(RetrieveAPIView):
    serializer_class = ProductUpdateCreateSerializer
    queryset = Product.objects.all()
    lookup_field = "pk"


class ProductUpdateAPI(RetrieveUpdateAPIView):
    serializer_class = ProductUpdateCreateSerializer
    queryset = Product.objects.all()
    lookup_field = "pk"


class ProductDestroyAPI(RetrieveDestroyAPIView):
    serializer_class = ProductListSerializer
    lookup_field = "pk"

    def get_queryset(self):
        return Product.objects.filter(is_active=False)
