
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^album/', include('album.urls')),

    url(r'register/', views.UserFormView.as_view(), name='register'),
    url(r'account_login/', views.LoginForm.as_view(), name='login'),
    url(r'account_logout/', views.LogoutView.as_view(), name='logout'),
    url(r'accounts/social/signup/', views.MySignupView.as_view(), name='singup'),
    url(r'^accounts/', include('allauth.urls')),

]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        url(r'__debug__', include(debug_toolbar.urls)),
    ]