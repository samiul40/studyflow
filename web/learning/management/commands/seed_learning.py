import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from faker import Faker

from learning.models import LearningResource, LearningUnit


class Command(BaseCommand):
    help = "Seed learning resources and units with fake data"

    def handle(self, *args, **kwargs):
        fake = Faker()

        User = get_user_model()
        user = User.objects.first()

        if not user:
            self.stdout.write(self.style.ERROR("No users found. Create a user first."))
            return

        self.stdout.write(self.style.SUCCESS("Creating learning resources..."))

        resources = []

        for _ in range(8):
            resource = LearningResource.objects.create(
                user=user,
                title=fake.sentence(nb_words=4),
                resource_type=random.choice(LearningResource.ResourceType.values),
                description=fake.text(max_nb_chars=120),
            )

            resources.append(resource)

        self.stdout.write(self.style.SUCCESS("Creating learning units..."))

        for resource in resources:
            unit_count = random.randint(5, 20)
            for i in range(1, unit_count + 1):
                status = random.choice(LearningUnit.StatusChoices.values)

                duration = None
                progress = None
                if resource.resource_type != LearningResource.ResourceType.BOOK:
                    duration = random.randint(5, 25)
                    progress = None

                    if status == LearningUnit.StatusChoices.IN_PROGRESS:
                        progress = random.randint(1, duration)

                    if status == LearningUnit.StatusChoices.COMPLETED:
                        progress = duration

                LearningUnit.objects.create(
                    resource=resource,
                    title=f"Unit {i}: {fake.sentence(nb_words=3)}",
                    order=i,
                    duration_minutes=duration,
                    status=status,
                    video_progress_minutes=progress,
                    notes=fake.text(max_nb_chars=80) if random.random() < 0.3 else "",
                )

        self.stdout.write(self.style.SUCCESS("Learning data successfully seeded!"))
