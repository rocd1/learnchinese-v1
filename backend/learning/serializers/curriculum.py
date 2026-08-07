from rest_framework import serializers

from learning.models import (
    HSKLevel,
    Lesson,
)


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = (
            "id",
            "title",
            "description",
            "order",
        )


class HSKLevelListSerializer(serializers.ModelSerializer):
    class Meta:
        model = HSKLevel
        fields = (
            "id",
            "level",
            "name",
            "total_words",
            "image",
        )


class HSKLevelDetailSerializer(serializers.ModelSerializer):

    lessons = LessonSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = HSKLevel
        fields = (
            "id",
            "level",
            "name",
            "description",
            "total_words",
            "image",
            "active",
            "lessons",
        )