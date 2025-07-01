from uuid import uuid4

from django.contrib.auth import get_user_model
from django.db import models

from reviews.validators import hexadecimal_color_validator, initial_date_validator


# Create your models here.
class Subject(models.Model):
    id = models.UUIDField(verbose_name="ID", primary_key=True, default=uuid4)
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name="User",
        related_name="subjects",
    )
    name = models.CharField(verbose_name="Name", max_length=255)
    color = models.CharField(
        verbose_name="Color",
        max_length=7,
        validators=[hexadecimal_color_validator],
    )

    class Meta:
        unique_together = (
            ("user", "name"),
            ("user", "color"),
        )
    
    def __str__(self):
        return f"{self.name} ({self.user})"


class ReviewInfo(models.Model):
    id = models.UUIDField(verbose_name="ID", primary_key=True, default=uuid4)
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name="User",
        related_name="reviews",
    )
    topic = models.CharField(verbose_name="Topic", max_length=255)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    notes = models.TextField(verbose_name="Notes", null=True, blank=True)
    initial_date = models.DateField(
        verbose_name="Initial Date",
        validators=[initial_date_validator],
    )

    def __str__(self):
        return f"{self.topic} ({self.user})"


class ReviewSchedule(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pendente"),
        ("completed", "Concluída"),
        ("skipped", "Ignorada"),
    ]

    review_info = models.ForeignKey(
        ReviewInfo,
        on_delete=models.CASCADE,
        related_name="schedules",
    )
    scheduled_for = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.review_info.topic} ({self.review_info.user}) - {self.scheduled_for}"
