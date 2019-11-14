from glob import glob
import os

from django.apps import AppConfig
from django.conf import settings


class CoreConfig(AppConfig):
    name = 'biscuit.core'
    verbose_name = 'BiscuIT - The Free School Information System'

    def clean_scss(self) -> None:
        for source_map in glob(os.path.join(settings.STATIC_ROOT, '*.css.map')):
            try:
                os.unlink(source_map)
            except OSError:
                # Ignore because old is better than nothing
                pass  # noqa

    def ready(self) -> None:
        self.clean_scss()