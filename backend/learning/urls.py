from django.urls import path

from learning.views import (
    HSKLevelListView,
    HSKLevelDetailView,
    VocabularyListView,
    VocabularyDetailView,
    LearnedWordListView,
    QuizResultListView,
    QuizResultDetailView,
)

from learning.views.favorite import (
    FavoriteListView,
    FavoriteToggleView,
)

from learning.views.learning import (
    LearningSessionAnswerView,
    LearningSessionView,
)


urlpatterns = [

    # ========================================================
    # HSK
    # ========================================================

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

    # ========================================================
    # VOCABULARY
    # ========================================================

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

    # ========================================================
    # LEARNING PROGRESS
    # ========================================================

    path(
        "learning/",
        LearnedWordListView.as_view(),
        name="learning-list",
    ),

    # ========================================================
    # FAVORITES
    # ========================================================

    path(
        "favorites/",
        FavoriteListView.as_view(),
        name="favorite-list",
    ),

    path(
        "favorites/toggle/",
        FavoriteToggleView.as_view(),
        name="favorite-toggle",
    ),

    # ========================================================
    # QUIZ RESULTS
    # ========================================================

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

    # ========================================================
    # LEARNING SESSION
    # ========================================================

    path(
        "learning/session/",
        LearningSessionView.as_view(),
        name="learning-session",
    ),

    path(
        "learning/session/answer/",
        LearningSessionAnswerView.as_view(),
        name="learning-session-answer",
    ),
]
