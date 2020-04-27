from datetime import datetime, timedelta
from itertools import groupby
from operator import itemgetter
import os
import pkgutil
from importlib import import_module
from typing import Any, Callable, Sequence, Union, List
from uuid import uuid4

from django.conf import settings
from django.db.models import Model
from django.http import HttpRequest
from django.utils import timezone
from django.utils.functional import lazy

from dynamic_preferences.registries import global_preferences_registry


def copyright_years(years: Sequence[int], seperator: str = ", ", joiner: str = "–") -> str:
    """ Takes a sequence of integegers and produces a string with ranges

    >>> copyright_years([1999, 2000, 2001, 2005, 2007, 2008, 2009])
    '1999–2001, 2005, 2007–2009'
    """

    ranges = [list(map(itemgetter(1), group)) for _, group in groupby(enumerate(years), lambda e: e[1]-e[0])]
    years_strs = [str(range_[0]) if len(range_) == 1 else joiner.join([str(range_[0]), str(range_[-1])]) for range_ in ranges]

    return seperator.join(years_strs)

def dt_show_toolbar(request: HttpRequest) -> bool:
    from debug_toolbar.middleware import show_toolbar  # noqa

    if not settings.DEBUG:
        return False

    if show_toolbar(request):
        return True
    elif hasattr(request, "user") and request.user.is_superuser:
        return True

    return False


def get_app_packages() -> Sequence[str]:
    """ Find all packages within the aleksis.apps namespace. """

    # Import error are non-fatal here because probably simply no app is installed.
    try:
        import aleksis.apps
    except ImportError:
        return []

    return ["aleksis.apps.%s" % pkg[1] for pkg in pkgutil.iter_modules(aleksis.apps.__path__)]


def merge_app_settings(setting: str, original: Union[dict, list], deduplicate: bool = False) -> Union[dict, list]:
    """ Get a named settings constant from all apps and merge it into the original.
    To use this, add a settings.py file to the app, in the same format as Django's
    main settings.py.

    Note: Only selected names will be imported frm it to minimise impact of
    potentially malicious apps!
    """

    for pkg in get_app_packages():
        try:
            mod_settings = import_module(pkg + ".settings")
        except ImportError:
            # Import errors are non-fatal. They mean that the app has no settings.py.
            continue

        app_setting = getattr(mod_settings, setting, None)
        if not app_setting:
            # The app might not have this setting or it might be empty. Ignore it in that case.
            continue

        for entry in app_setting:
            if entry in original:
                if not deduplicate:
                    raise AttributeError("%s already set in original." % entry)
            else:
                if isinstance(original, list):
                    original.append(entry)
                elif isinstance(original, dict):
                    original[entry] = app_setting[entry]
                else:
                    raise TypeError("Only dict and list settings can be merged.")


def lazy_preference(section: str, name: str) -> Callable[[str, str], Any]:
    """ Lazily get a config value from dynamic preferences. Useful to bind preferences
    to other global settings to make them available to third-party apps that are not
    aware of dynamic preferences.
    """

    def _get_preference(section: str, name: str) -> Any:
        return global_preferences["%s__%s" % (section, name)]

    # The type is guessed from the default value to improve lazy()'s behaviour
    # FIXME Reintroduce the behaviour described above
    return lazy(_get_preference, str)(section, name)


def is_impersonate(request: HttpRequest) -> bool:
    if hasattr(request, "user"):
        return getattr(request.user, "is_impersonate", False)
    else:
        return False


def has_person(obj: Union[HttpRequest, Model]) -> bool:
    """ Check wehether a model object has a person attribute linking it to a Person
    object. The passed object can also be a HttpRequest object, in which case its
    associated User object is unwrapped and tested.
    """

    if isinstance(obj, HttpRequest):
        if hasattr(obj, "user"):
            obj = obj.user
        else:
            return False

    return getattr(obj, "person", None) is not None


def celery_optional(orig: Callable) -> Callable:
    """ Decorator that makes Celery optional for a function.

    If Celery is configured and available, it wraps the function in a Task
    and calls its delay method when invoked; if not, it leaves it untouched
    and it is executed synchronously.
    """

    if hasattr(settings, "CELERY_RESULT_BACKEND"):
        from ..celery import app  # noqa
        task = app.task(orig)

    def wrapped(*args, **kwargs):
        if hasattr(settings, "CELERY_RESULT_BACKEND"):
            task.delay(*args, **kwargs)
        else:
            orig(*args, **kwargs)

    return wrapped


def path_and_rename(instance, filename: str, upload_to: str = "files") -> str:
    """ Updates path of an uploaded file and renames it to a random UUID in Django FileField """

    _, ext = os.path.splitext(filename)

    # set filename as random string
    new_filename = '{}.{}'.format(uuid4().hex, ext)

    # Create upload directory if necessary
    os.makedirs(os.path.join(settings.MEDIA_ROOT, upload_to), exist_ok=True)

    # return the whole path to the file
    return os.path.join(upload_to, new_filename)


def custom_information_processor(request: HttpRequest) -> dict:
    """ Provides custom information in all templates """

    from ..models import School, CustomMenu
    return {
        "SCHOOL": School.get_default,
        "FOOTER_MENU": CustomMenu.get_default("footer"),
    }


def now_tomorrow() -> datetime:
    """ Return current time tomorrow """
    return timezone.now() + timedelta(days=1)
