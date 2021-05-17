from django.contrib import admin
from django.urls import path,include
from store import views
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name="home"),
    path('collection/<slug:collection_slug>',views.home,name="product_by_collection"),
    path('product/<slug:collection_slug>/<slug:product_slug>',views.productPage,name='productDetail'),
    path('cart/add/<int:product_id>',views.addCart,name="addCart"),
    path('cartdetail/',views.cartdetail,name="cartdetail"),
    path('cart/remove/<int:product_id>',views.removeCart,name="removeCart"),
    path('about',views.about,name="about"),
    path('signup',views.signup,name="signup"),
    path('thankyou',views.thankyou,name="thankyou"),
    path('accounts/', include('allauth.urls')),

]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    
    
