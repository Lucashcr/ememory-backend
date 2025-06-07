from datetime import date

from django.core.management.base import BaseCommand

from reviews.models import ReviewSchedule


class Command(BaseCommand):
    help = "Skip all pending review schedules that are scheduled for today or earlier."

    def handle(self, *args, **options):
        schedules = ReviewSchedule.objects.filter(
            status="pending",
            scheduled_for__lt=date.today(),
        )

        count = schedules.count()

        if count == 0:
            self.stdout.write(
                self.style.SUCCESS("No pending review schedules to skip.")
            )
            return

        schedules.update(status="skipped")
        self.stdout.write(
            self.style.SUCCESS(f"Skipped {count} pending review schedules.")
        )
