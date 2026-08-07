from rest_framework import serializers

from learning.models import (
    Character,
    ExampleSentence,
    GrammarPoint,
    Lesson,
    Vocabulary,
)


class ExampleSentenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExampleSentence
        fields = (
            "sentence",
            "pinyin",
            "translation",
        )


class CharacterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Character
        fields = (
            "character",
            "practice_writing",
            "order",
        )


class GrammarPointSerializer(serializers.ModelSerializer):

    class Meta:
        model = GrammarPoint
        fields = (
            "id",
            "title",
            "explanation",
            "order",
        )


class LessonMiniSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = (
            "id",
            "title",
            "order",
        )


class VocabularyListSerializer(serializers.ModelSerializer):

    level = serializers.IntegerField(
        source="hsk_level.level",
        read_only=True,
    )

    class Meta:
        model = Vocabulary
        fields = (
            "id",
            "hsk_id",
            "simplified",
            "traditional",
            "pinyin",
            "meaning",
            "level",
            "slug",
        )


class VocabularyDetailSerializer(serializers.ModelSerializer):

    level = serializers.IntegerField(
        source="hsk_level.level",
        read_only=True,
    )

    examples = ExampleSentenceSerializer(
        many=True,
        read_only=True,
    )

    lessons = LessonMiniSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Vocabulary
        fields = (
            "id",
            "hsk_id",
            "simplified",
            "traditional",
            "pinyin",
            "pinyin_plain",
            "meaning",
            "notes",
            "audio",
            "slug",
            "level",
            "examples",
            "lessons",
        )