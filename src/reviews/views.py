import datetime

from django.http import JsonResponse
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from reviews.constants import INTERVALS
from reviews.models import ReviewInfo, ReviewSchedule
from reviews.serializers import ReviewInfoSerializer, SubjectSerializer


# Create your views here.
class SubjectsViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SubjectSerializer

    def get_queryset(self):
        return self.request.user.subjects.all()

    def perform_create(self, serializer):
        serializer.validated_data["user_id"] = self.request.user.id
        return super().perform_create(serializer)


class ReviewInfoViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewInfoSerializer

    def get_queryset(self):
        return self.request.user.reviews.all()

    def perform_create(self, serializer: ReviewInfoSerializer):
        mark_first = serializer.validated_data.pop("mark_first")
        review_info = ReviewInfo.objects.create(
            **serializer.validated_data,
            user_id=self.request.user.id,
        )

        for interval in INTERVALS:
            scheduled_date = review_info.initial_date + datetime.timedelta(days=interval)
            ReviewSchedule.objects.create(
                review_info=review_info,
                scheduled_for=scheduled_date,
                status="completed" if interval == 0 and mark_first else "pending",
            )

    def perform_update(self, serializer: ReviewInfoSerializer):
        mark_first = serializer.validated_data.pop("mark_first")
        super().perform_update(serializer)

        instance = ReviewInfo.objects.get(id=self.kwargs["pk"])
        schedules = instance.schedules.all()
        for interval, schedule in zip(INTERVALS, schedules):
            scheduled_date = instance.initial_date + datetime.timedelta(days=interval)
            schedule.scheduled_for = scheduled_date
            schedule.status = "completed" if interval == 0 and mark_first else "pending"
        ReviewSchedule.objects.bulk_update(schedules, ["scheduled_for", "status"])

    @action(detail=True, methods=["patch"], url_path="status")
    def update_status(self, request, pk=None):
        review_info = ReviewInfo.objects.filter(user=request.user, id=pk).first()
        if not review_info:
            return JsonResponse({"error": "Review not found"}, status=404)

        status = request.data.get("status")
        if status not in ["pending", "completed", "skipped"]:
            return JsonResponse({"error": "Invalid status"}, status=400)

        date = request.data.get("date")
        if not date:
            return JsonResponse({"error": "Date is required"}, status=400)
        if date != datetime.date.today().strftime("%Y-%m-%d"):
            return JsonResponse({"error": "Date must be today"}, status=400)

        review_schedule = review_info.schedules.filter(scheduled_for=date).first()
        if not review_schedule:
            return JsonResponse({"error": "Schedule not found"}, status=404)

        review_schedule.status = status
        review_schedule.save()
        return JsonResponse(self.serializer_class(review_info).data, status=200)
