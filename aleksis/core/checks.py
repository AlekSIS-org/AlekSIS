from typing import Optional

import django.apps
from django.core.checks import Tags, Warning, register

from .mixins import ExtensibleModel, PureDjangoModel
from .util.apps import AppConfig


@register(Tags.compatibility)
def check_app_configs_base_class(
    app_configs: Optional[django.apps.registry.Apps] = None, **kwargs
) -> None:
    """ Checks whether all apps derive from AlekSIS's base app config """

    results = []

    if app_configs is None:
        app_configs = django.apps.apps.get_app_configs()

    for app_config in app_configs:
        if app_config.name.startswith("aleksis.apps.") and not isinstance(app_config, AppConfig):
            results.append(
                Warning(
                    "App config %s does not derive from aleksis.core.util.apps.AppConfig.",
                    hint="Ensure the app uses the correct base class for all registry functionality to work.",
                    obj=app_config,
                    id="aleksis.core.W001",
                )
            )

    return results


@register(Tags.compatibility)
def check_app_models_base_class(
    app_configs: Optional[django.apps.registry.Apps] = None, **kwargs
) -> list:
    """ Checks whether all app models derive from AlekSIS's base ExtensibleModel """

    results = []

    if app_configs is None:
        app_configs = django.apps.apps.get_app_configs()

    for app_config in filter(lambda c: c.name.startswith("aleksis."), app_configs):
        for model in app_config.get_models():
            if ExtensibleModel not in model.__mro__ and PureDjangoModel not in model.__mro__:
                results.append(
                    Warning(
                        "Model %s in app config %s does not derive from aleksis.core.mixins.ExtensibleModel." % (model._meta.object_name, app_config.name),
                        hint="Ensure all models in AlekSIS use ExtensibleModel as base. If your deviation is intentional, you can add the PureDjangoModel mixin instead to silence this warning.",
                        obj=model,
                        id="aleksis.core.W002",
                    )
                )

    return results
