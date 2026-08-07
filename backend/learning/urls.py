from django.urls import path

from learning.views import (
    HSKLevelListView,
    HSKLevelDetailView,
    VocabularyListView,
    VocabularyDetailView,
    LearnedWordListView,
    FavoriteWordListView,
    QuizResultListView,
    QuizResultDetailView,
)

urlpatterns = [

    # ---------------------------------------------------------
    # HSK
    # ---------------------------------------------------------

    path(
        "hsk/",
        HSKLevelListView.as_view(),
        name="hsk-list",
    ),

    path(
        "hsk/<int:pk>/",
        HSKLevelDetailView.as_view(),
        name="hsk-detail",
    ),

    # ---------------------------------------------------------
    # Vocabulary
    # ---------------------------------------------------------

    path(
        "vocabulary/",
        VocabularyListView.as_view(),
        name="vocabulary-list",
    ),

    path(
        "vocabulary/<int:pk>/",
        VocabularyDetailView.as_view(),
        name="vocabulary-detail",
    ),

    # ---------------------------------------------------------
    # Learning
    # ---------------------------------------------------------

    path(
        "learning/",
        LearnedWordListView.as_view(),
        name="learning-list",
    ),

    path(
        "favorites/",
        FavoriteWordListView.as_view(),
        name="favorite-list",
    ),

    # ---------------------------------------------------------
    # Quiz
    # ---------------------------------------------------------

    path(
        "quiz-results/",
        QuizResultListView.as_view(),
        name="quiz-result-list",
    ),

    path(
        "quiz-results/<int:pk>/",
        QuizResultDetailView.as_view(),
        name="quiz-result-detail",
    ),
]