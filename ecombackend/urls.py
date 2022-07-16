"""ecombackend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from order.views import cartItem, remove_single_item_from_cart, wishItem, remove_single_item_from_wishlist, coupon_use, \
    remove_whole_item_from_cart, Checkout, dropLocation
from product.views import allProductView, categoryProductView, singleProductView, searchProduct, subcategoryProductView
from user.views import Login_User, Create_User, forgetpw, activate, activatepw, logouts, details, changepass

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/login/', Login_User.as_view(), name="login"),
    path('api/v1/Register/', Create_User.as_view(), name="register"),
    # path('api/v1/userdata/<int:id>/', signup.as_view(), name="userdata"),
    path('api/v1/forgetpw/<int:id>/', forgetpw.as_view(), name="forgetpassword"),
    path('api/v1/activate/<uidb64>/<token>/', activate, name='activate'),
    path('api/v1/activatepw/<uidb64>/<token>/', activatepw, name='password reset'),
    path('api/v1/product/', allProductView.as_view(), name="all product"),
    path('api/v1/product/category/', categoryProductView.as_view(), name="category product"),
    path('api/v1/product/subcategory/', subcategoryProductView.as_view(), name="sub category"),
    path('api/v1/logout/', logouts),
    path('api/v1/userdetails/', details.as_view(), name="user details"),
    path('api/v1/changepassword/', changepass.as_view(), name="change password"),
    path('api/v1/forgetpassword/', forgetpw.as_view(), name="forget password"),
    path('api/v1/cart/', cartItem.as_view(), name="Cart items"),
    path('api/v1/removeitem/', remove_single_item_from_cart.as_view(), name="remove item"),
    path('api/v1/wishitem/', wishItem.as_view(), name="wish item"),
    path('api/v1/removewish/', remove_single_item_from_wishlist.as_view(), name="remove wish"),
    path('api/v1/coupon/', coupon_use.as_view(), name="coupon use"),
    path('api/v1/unique/product/', singleProductView.as_view(), name="Single Product"),
    path('api/v1/removeall/', remove_whole_item_from_cart.as_view(), name="Remove Product"),
    path('api/v1/location/', dropLocation.as_view(), name="Drop Location"),
    path('api/v1/checkout/', Checkout.as_view(), name="Check Out"),
    path('api/v1/search/', searchProduct.as_view(), name="Search"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
