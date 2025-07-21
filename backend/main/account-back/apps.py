from django.apps import AppConfig
from django.db.models.signals import post_migrate
 

class AccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'account'
    def ready(self):
            
            from account.utils.groups import CareerWaderGroupManager 

            def create_groups(sender, **kwargs):
                manager = CareerWaderGroupManager()
                manager.create_groups()

                # manager.assign_permissions("Vendor", [
                #     ("orders", "add_order"),
                #     ("orders", "view_order"),
                # ])
                # manager.assign_permissions("Vendor", [
                #     ("orders", "add_order"),
                #     ("orders", "view_order"),
                # ])
                # manager.assign_permissions("Vendor", [
                #     ("orders", "add_order"),
                #     ("orders", "view_order"),
                # ])
                # manager.assign_permissions("Vendor", [
                #     ("orders", "add_order"),
                #     ("orders", "view_order"),
                # ])


            post_migrate.connect(create_groups, sender=self)