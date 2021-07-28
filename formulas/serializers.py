import re

from django.core.validators import slug_re
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from formulas.models import (
    Photo,
    PhotoClassification,
    PhotoContext,
    Profile,
    Review,
    Subject,
    Tag,
)
from formulas.serializer_extra_fields import (
    HybridImageField,
    SlugGetOrCreateRelatedField,
)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            "pk",
            "user",
            "career_name",
        )
        read_only_fields = ("user",)


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = (
            "pk",
            "name",
        )


def validate_subject_slug(value):
    if not re.match(slug_re, value):
        raise serializers.ValidationError(
            _(
                "Enter a valid “slug” consisting of letters, numbers, underscores or hyphens."
            )
        )


class PhotoClassificationSerializer(serializers.ModelSerializer):

    subject = SlugGetOrCreateRelatedField(
        queryset=Subject.objects.all(),
        slug_field="name",
        required=True,
        internal_validators=[validate_subject_slug],
    )

    class Meta:
        model = PhotoClassification
        fields = (
            "pk",
            "subject",
            "exam_number",
        )

    def create(self, validated_data):
        # Multiple object error cannot happen unless you modify the db
        # get or create return a tuple (instance, bool: created or not)
        return PhotoClassification.objects.get_or_create(
            subject=validated_data["subject"], exam_number=validated_data["exam_number"]
        )[0]


class PhotoContextSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoContext
        fields = (
            "pk",
            "formula_type",
            "professor",
        )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            "pk",
            "name",
        )


class PhotoSerializer(serializers.ModelSerializer):

    user = serializers.ReadOnlyField(source="user.pk")
    tags = SlugGetOrCreateRelatedField(
        many=True, slug_field="name", queryset=Tag.objects.all(), required=False
    )
    file = HybridImageField(allow_null=True, required=False)
    photo_classification = PhotoClassificationSerializer()
    photo_context = PhotoContextSerializer(required=False)

    def create(self, validated_data):

        # there is no need to validate the serializers
        # they were already validated by PhotoSerializer

        photo_classification_data = validated_data.pop("photo_classification")
        s = PhotoClassificationSerializer()
        photo_classification = s.create(photo_classification_data)
        validated_data["photo_classification"] = photo_classification

        if "photo_context" in validated_data:
            photo_context_data = validated_data.pop("photo_context")
            s = PhotoContextSerializer()
            photo_context = s.create(photo_context_data)
            validated_data["photo_context"] = photo_context

        photo_tags = validated_data.pop("tags", [])
        photo = Photo.objects.create(**validated_data)
        photo.tags.add(*photo_tags)

        return photo

    def update(self, instance, validated_data):

        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.description)

        if "file" in validated_data:
            instance.file.delete()
            instance.file = validated_data["file"]

        photo_classification_new_data = validated_data.get("photo_classification", None)

        if photo_classification_new_data:
            photo_classification_data = {
                "subject": instance.photo_classification.subject,
                "exam_number": instance.photo_classification.exam_number,
            }
            photo_classification_data.update(photo_classification_new_data)

            s = PhotoClassificationSerializer()
            photo_classification = s.create(photo_classification_data)
            instance.photo_classification = photo_classification

        if "photo_context" in validated_data:
            photo_context_data = validated_data["photo_context"]
            if instance.photo_context:
                instance.photo_context.professor = photo_context_data.get(
                    "professor", instance.photo_context.professor
                )
                instance.photo_context.formula_type = photo_context_data.get(
                    "formula_type", instance.photo_context.formula_type
                )
                instance.photo_context.save()
            else:
                instance.photo_context = PhotoContext.objects.create(
                    **photo_context_data
                )

        if "tags" in validated_data:
            instance.tags.set(validated_data["tags"])

        instance.save()
        return instance

    class Meta:
        model = Photo
        fields = (
            "pk",
            "name",
            "file",
            "description",
            "photo_classification",
            "photo_context",
            "user",
            "tags",
            "created_at",
            "updated_at",
        )


class ReviewSerializer(serializers.ModelSerializer):

    user = serializers.ReadOnlyField(source="user.pk")

    def validate(self, data):
        if "photo" in data:
            user = self.context["request"].user
            if user == data["photo"].user:
                raise serializers.ValidationError(_("Photo owner cannot make a review"))

        return data

    class Meta:
        model = Review
        fields = (
            "pk",
            "stars",
            "photo",
            "user",
        )
