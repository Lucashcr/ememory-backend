from rest_framework.serializers import ModelSerializer, UUIDField, CharField

from reviews.models import ReviewInfo, ReviewSchedule, Subject


class SubjectSerializer(ModelSerializer):
    class Meta:
        model = Subject
        fields = ["id", "name", "color"]


class ReviewInfoSerializer(ModelSerializer):
    class ReviewDatesSerializer(ModelSerializer):
        class Meta:
            model = ReviewSchedule
            fields = ["scheduled_for", "status"]

    review_dates = ReviewDatesSerializer(
        many=True,
        read_only=True,
        source="schedules",
    )
    subject = SubjectSerializer(
        read_only=True,
    )
    subject_id = UUIDField(
        write_only=True,
    )

    class Meta:
        model = ReviewInfo
        fields = ["id", "topic", "subject", "subject_id", "notes", "initial_date", "review_dates"]
        read_only_fields = ["subject", "review_dates"]
        write_only_fields = ["subject_id"]
