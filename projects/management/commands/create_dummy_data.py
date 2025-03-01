from django.core.management.base import BaseCommand
from faker import Faker
from projects.models import Project, Tag
from users.models import Profile
from datetime import datetime

class Command(BaseCommand):
    help = 'Create dummy projects and developers'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Create dummy developers
        for _ in range(5):
            profile = Profile.objects.create(
                name=fake.name(),
                email=fake.email(),
                username=fake.user_name(),
                bio=fake.text(),
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully created developer {profile.name}'))

        # Create dummy tags
        for _ in range(5):
            tag = Tag.objects.create(
                name=fake.word(),
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully created tag {tag.name}'))

        # Create dummy projects
        for _ in range(5):
            project = Project.objects.create(
                title=fake.sentence(nb_words=6),  # Ensure the title is a short sentence
                description=fake.text(max_nb_chars=200),  # Ensure the description is not too long
                owner=Profile.objects.order_by('?').first(),  # Assign a random developer
                featured_images="images/default.jpg",  # Use a default image path
                demo_link=fake.url(),  # Generate a random URL for demo_link
                source_link=fake.url(),  # Generate a random URL for source_link
                vote_total=fake.random_int(min=0, max=100),  # Generate a random integer for vote_total
                vote_ratio=fake.random_int(min=0, max=100),  # Generate a random integer for vote_ratio
                created_at=fake.date_time_this_year(),  # Generate a random datetime within this year
                updated_at=fake.date_time_this_year(),  # Generate a random datetime within this year
            )
            project.tags.add(*Tag.objects.order_by('?')[:3])  # Assign random tags
            self.stdout.write(self.style.SUCCESS(f'Successfully created project {project.title}'))