from rest_framework import serializers

from learning.models import HSKLevel, QuizResult, Vocabulary


# ============================================================
# GUEST QUIZ START
# ============================================================


class GuestQuizStartSerializer(serializers.Serializer):
    """
    Validate a request to start a guest practice quiz.
    """

    quiz_type = serializers.ChoiceField(
        choices=QuizResult.QuizType.choices,
    )

    hsk_level = serializers.PrimaryKeyRelatedField(
        queryset=HSKLevel.objects.filter(
            active=True,
        ),
    )

    total_questions = serializers.IntegerField(
        min_value=1,
        max_value=10,
    )

    typing_mode = serializers.ChoiceField(
        choices=QuizResult.TypingMode.choices,
        required=False,
        allow_blank=True,
    )

    def validate(self, attrs):
        quiz_type = attrs["quiz_type"]

        typing_mode = attrs.get(
            "typing_mode",
            "",
        )

        supported_quiz_types = {
            QuizResult.QuizType.FLASHCARD,
            QuizResult.QuizType.MATCHING,
            QuizResult.QuizType.TYPING,
            QuizResult.QuizType.WORD_TILE,
        }

        typing_modes = {
            QuizResult.TypingMode.MEANING_TO_CHINESE,
            QuizResult.TypingMode.CHINESE_TO_PINYIN,
        }

        if quiz_type not in supported_quiz_types:
            raise serializers.ValidationError(
                {
                    "quiz_type": (
                        "This guest quiz type is not currently supported."
                    )
                }
            )

        if quiz_type == QuizResult.QuizType.TYPING:
            if typing_mode not in typing_modes:
                raise serializers.ValidationError(
                    {
                        "typing_mode": (
                            "A valid typing mode is required "
                            "for typing quizzes."
                        )
                    }
                )

        elif typing_mode:
            raise serializers.ValidationError(
                {
                    "typing_mode": (
                        "typing_mode can only be used "
                        "with typing quizzes."
                    )
                }
            )

        return attrs


# ============================================================
# GUEST QUIZ ANSWER
# ============================================================


class GuestQuizAnswerSerializer(serializers.Serializer):
    """
    Validate a guest quiz answer.
    """

    vocabulary = serializers.PrimaryKeyRelatedField(
        queryset=Vocabulary.objects.all(),
    )

    user_answer = serializers.CharField(
        max_length=255,
        allow_blank=False,
        trim_whitespace=True,
    )


# ============================================================
# GUEST QUIZ ANSWER RESPONSE
# ============================================================


class GuestQuizAnswerResponseSerializer(
    serializers.Serializer,
):
    """
    Response returned after submitting a guest answer.
    """

    vocabulary = serializers.IntegerField()

    user_answer = serializers.CharField()

    correct_answer = serializers.CharField()

    is_correct = serializers.BooleanField()


# ============================================================
# GUEST QUIZ QUESTION
# ============================================================


class GuestQuizQuestionSerializer(
    serializers.ModelSerializer,
):
    """
    Serializer for questions presented to a guest.
    """

    class Meta:
        model = Vocabulary

        fields = (
            "id",
            "simplified",
            "pinyin",
            "meaning",
        )

    def to_representation(self, instance):
        quiz_type = self.context.get(
            "quiz_type",
        )

        typing_mode = self.context.get(
            "typing_mode",
            "",
        )

        if quiz_type == QuizResult.QuizType.FLASHCARD:
            return {
                "id": instance.id,
                "simplified": instance.simplified,
                "pinyin": instance.pinyin,
                "meaning": instance.meaning,
            }

        if quiz_type == QuizResult.QuizType.MATCHING:
            return {
                "id": instance.id,
                "simplified": instance.simplified,
                "meaning": instance.meaning,
            }

        if quiz_type == QuizResult.QuizType.TYPING:

            if (
                typing_mode
                == QuizResult.TypingMode.MEANING_TO_CHINESE
            ):
                return {
                    "id": instance.id,
                    "meaning": instance.meaning,
                }

            if (
                typing_mode
                == QuizResult.TypingMode.CHINESE_TO_PINYIN
            ):
                return {
                    "id": instance.id,
                    "simplified": instance.simplified,
                }

        if quiz_type == QuizResult.QuizType.WORD_TILE:
            return {
                "id": instance.id,
                "simplified": instance.simplified,
            }

        raise serializers.ValidationError(
            "Unsupported guest quiz type."
        )