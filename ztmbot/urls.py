from django.contrib import admin
from django.urls import path
from .quiz.views import RandomQuestion
from .score.views import UpdateScores


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/random/', RandomQuestion.as_view(), name='random'),
    path('api/score/update/', UpdateScores.as_view(), name='score_update'),
]
