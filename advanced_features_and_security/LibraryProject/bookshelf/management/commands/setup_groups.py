# bookshelf/management/commands/setup_groups.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from bookshelf.models import Book

class Command(BaseCommand):
    help = "Create default groups and assign permissions"

    def handle(self, *args, **kwargs):
        # Create groups
        viewers, _ = Group.objects.get_or_create(name="Viewers")
        editors, _ = Group.objects.get_or_create(name="Editors")
        admins, _ = Group.objects.get_or_create(name="Admins")

        # Get the content type for Book model
        content_type = ContentType.objects.get_for_model(Book)

        # Get permissions
        can_view = Permission.objects.get(codename="can_view", content_type=content_type)
        can_create = Permission.objects.get(codename="can_create", content_type=content_type)
        can_edit = Permission.objects.get(codename="can_edit", content_type=content_type)
        can_delete = Permission.objects.get(codename="can_delete", content_type=content_type)

        # Assign permissions to groups
        viewers.permissions.set([can_view])
        editors.permissions.set([can_view, can_create, can_edit])
        admins.permissions.set([can_view, can_create, can_edit, can_delete])

        self.stdout.write(self.style.SUCCESS("Groups and permissions successfully created!"))
