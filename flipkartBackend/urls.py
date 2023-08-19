from django.urls import path
from .settings import BASE_DIR
from .views import TopRatedProduct,TopSimilaryProduct,findRecentProduct
urlpatterns = [
    path("products/<int:limit>/",TopRatedProduct),
    path("products/",TopRatedProduct),
    path("products/similar/<str:product_id>/<int:limit>/",TopSimilaryProduct),
    path("products/similar/<str:product_id>/",TopSimilaryProduct),
    path("products/recent/<str:user_id>/<int:limit>/",findRecentProduct),
    path("products/recent/<str:user_id>/",findRecentProduct),
]

