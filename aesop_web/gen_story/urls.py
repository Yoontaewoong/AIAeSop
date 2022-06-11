from gen_story.views import Generate
from django.urls import path, include

urlpatterns = [
    path('generate', Generate.as_view(), name = "generate")
]