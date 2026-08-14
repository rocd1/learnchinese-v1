from django.urls import path

from learning.views import (
    HSKLevelListView,
    HSKLevelDetailView,
    VocabularyListView,
    VocabularyDetailView,
    LearnedWordListView,
    QuizResultListView
)

from learning.views.favorite import (
    FavoriteListView,
    FavoriteToggleView,
)

from learning.views.learning import (
    LearningSessionAnswerView,
    LearningSessionView,
)

from learning.views.dashboard import (
    DashboardStatisticsView,
)

from learning.views.quiz import (
    QuizAnswerView,
    QuizCompleteView,
    QuizStartView,
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


    # ============================================================
    # DASHBOARD
    # ============================================================

    path(
        "dashboard/statistics/",
        DashboardStatisticsView.as_view(),
        name="dashboard-statistics",
    ),

    # ============================================================
    # QUIZ
    # ============================================================

    path(
        "quiz/start/",
        QuizStartView.as_view(),
        name="quiz-start",
    ),

    path(
        "quiz/<int:pk>/answer/",
        QuizAnswerView.as_view(),
        name="quiz-answer",
    ),

    path(
        "quiz/<int:pk>/complete/",
        QuizCompleteView.as_view(),
        name="quiz-complete",
    ),


]
