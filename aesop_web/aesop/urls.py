from django.urls import path
from . import views

app_name = 'aesop'

urlpatterns = [
    path('', views.index, name='index'),
    path('page1/<int:story_id>', views.page1, name='page1'),
    # path('page2/<int:story_id>', views.page2, name='page2'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('question/create/', views.question_create, name='question_create'),
    path('recode', views.recode, name='recode'),
    path('creat_text', views.creat_text, name='creat_text'),
    path('creat_image', views.creat_image, name='creat_image'),
    path('page2', views.page2, name='page2'),
]
