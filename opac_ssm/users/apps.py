from django.apps import AppConfig
from django.db.models import signals


class UsersConfig(AppConfig):
    name = 'opac_ssm.users'
    verbose_name = "Users"

    def ready(self):
        """Override this to put in:
            Users system checks
            Users signal registration
        """
        from tastypie.models import create_api_key
        signals.post_save.connect(
            create_api_key,
            sender=self.get_model('User'))
