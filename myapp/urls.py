from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),                    # Home page
    path('signup/', views.signup, name='signup'),           # Sign Up page
    path('login/', views.login_view, name='login'),         # Login page
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),  # Logout
    path('about/', views.about, name='about'),
     path('classification/', views.new_classification, name='newclassification'),
    path('predict/', views.predict, name='predict'),
    path('records/', views.records, name='records'),
    path('profile/', views.profile_view, name='profile'),
    path('appsettings/', views.appsettings_view, name='appsettings'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)