from django.core.management import BaseCommand
from django.utils import timezone
from task_manager.tasks.models import Task


class Command(BaseCommand):
    help = 'Deletes expired tasks from the Database!'

    def handle(self, *args, **options):
        expired_tasks = Task.objects.filter(due_date__lt=timezone.now() - timezone.timedelta(weeks=2))
        expired_tasks.delete()
        self.stdout.write(self.style.SUCCESS('Expired tasks deleted successfully!'))
