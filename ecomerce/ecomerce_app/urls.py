from django.urls import path, include
from .views import*
from ecomerce_app import views
from rest_framework import routers
routers = routers.DefaultRouter()
routers.register('categories', views.CategoriesViewSet, "Categories")
routers.register('subcategories', views.SubCategoriesViewSet, "Sub-categories")
routers.register('products', views.ProductsViewSet, "Products")
routers.register('product/media', views.ProductMediaViewSet, "Product Media")
routers.register('product/details', views.ProductDetailsViewSet, "Product Details")
routers.register('product/quetions', views.ProductQuestionsViewSet, "Product Questions")
routers.register('product/reviews', views.ProductReviewsViewSet, "Product Reviews")
routers.register('product/review/votings', views.ProductReviewVotingViewSet, "Product Review Votings")
routers.register('product/transactions', views.ProductTransactionViewSet, "Product Transactions")
routers.register('customer/order', views.CustomerOrdersViewSet, "Customer Orders")
routers.register('delivery/status', views.OrderDeliveryStatusViewSet, "Delivery Status")

urlpatterns = [
    path('', include(routers.urls)),
    path('register', UserRegistrationView.as_view(), name='User Registration'),
    path('verify', VerifyOtp.as_view(), name='Email Verification'),
    path('login', UserLoginView.as_view(), name='User login'),
    path('list', UserListView.as_view(), name='Users'),
    path('forgot/password', ForgotPasswordView.as_view(), name='Forgot Password'),
    path('reset/password', ResetPasswordView.as_view(), name='Reset Password'),
    path('update/<int:pk>/', UpdateView.as_view(), name='Update and delete Profile'),

]