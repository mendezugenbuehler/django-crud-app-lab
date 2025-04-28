from django.core.management.base import BaseCommand
from main_app.models import Dog
from django.db.models import Count

class Command(BaseCommand):
    help = 'Removes duplicate dog records'

    def handle(self, *args, **options):
        # Find duplicates based on name, breed, description, age, and user
        duplicates = Dog.objects.values('name', 'breed', 'description', 'age', 'user').annotate(
            count=Count('id')
        ).filter(count__gt=1)

        for duplicate in duplicates:
            # Get all dogs matching these criteria
            dogs = Dog.objects.filter(
                name=duplicate['name'],
                breed=duplicate['breed'],
                description=duplicate['description'],
                age=duplicate['age'],
                user=duplicate['user']
            )
            # Keep the first one and delete the rest
            keep = dogs.first()
            dogs.exclude(id=keep.id).delete()
            self.stdout.write(f'Removed duplicates for {keep.name}') 