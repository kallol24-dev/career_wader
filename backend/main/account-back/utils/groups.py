from django.contrib.auth.models import Group, Permission

class CareerWaderGroupManager:
    def __init__(self):
        self.group_names = ["Councelor", "Student", "Franchaise", "Admin"]

    def create_groups(self):
        for name in self.group_names:
            group, created = Group.objects.get_or_create(name=name)
            if created:
                print(f"Group '{name}' created.")
            else:
                print(f"Group '{name}' already exists.")

    def add_permissions(self):
        for name in self.group_names:
            group = Group.objects.get(name=name)
            if group:
                permissions = Permission.objects.filter(codename__startswith=name.lower())
                group.permissions.set(permissions)
    def assign_permissions(self, group_name, permissions_list):
        
        try:
            group = Group.objects.get(name=group_name)
            for app_label, codename in permissions_list:
                perm = Permission.objects.get(content_type__app_label=app_label, codename=codename)
                group.permissions.add(perm)
            print(f"Permissions assigned to '{group_name}'.")
        except Group.DoesNotExist:
            print(f"Group '{group_name}' does not exist.")
        except Permission.DoesNotExist:
            print(f"One or more permissions not found.")

    def clear_permissions(self, group_name):
        try:
            group = Group.objects.get(name=group_name)
            group.permissions.clear()
            print(f"Cleared all permissions from group '{group_name}'.")
        except Group.DoesNotExist:
            print(f"Group '{group_name}' does not exist.")
        except Permission.DoesNotExist:
            print(f"One or more permissions not found.")