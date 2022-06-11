from django.contrib import admin
from django.urls import path, include
from aesop import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('aesop/', include('aesop.urls')),
    path('common/', include('common.urls')),
    path('', views.index, name='index'), # '/' 에 해당되는 path
    path('gen_story/', include('gen_story.urls')),
]
