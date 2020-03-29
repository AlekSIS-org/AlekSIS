import os
import sys
from glob import glob

from django.utils.translation import gettext_lazy as _
from calendarweek.django import i18n_day_name_choices_lazy

from dynaconf import LazySettings
from easy_thumbnails.conf import Settings as thumbnail_settings

from .util.core_helpers import get_app_packages, lazy_config, merge_app_settings
from .util.notifications import get_notification_choices_lazy

ENVVAR_PREFIX_FOR_DYNACONF = "ALEKSIS"
DIRS_FOR_DYNACONF = ["/etc/aleksis"]

SETTINGS_FILE_FOR_DYNACONF = []
for directory in DIRS_FOR_DYNACONF:
    SETTINGS_FILE_FOR_DYNACONF += glob(os.path.join(directory, "*.ini"))
    SETTINGS_FILE_FOR_DYNACONF += glob(os.path.join(directory, "*.yaml"))
    SETTINGS_FILE_FOR_DYNACONF += glob(os.path.join(directory, "*.toml"))

_settings = LazySettings(
    ENVVAR_PREFIX_FOR_DYNACONF=ENVVAR_PREFIX_FOR_DYNACONF,
    SETTINGS_FILE_FOR_DYNACONF=SETTINGS_FILE_FOR_DYNACONF,
)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = _settings.get("secret_key", "DoNotUseInProduction")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = _settings.get("maintenance.debug", False)
INTERNAL_IPS = _settings.get("maintenance.internal_ips", [])
DEBUG_TOOLBAR_CONFIG = {
    "RENDER_PANELS": True,
    "SHOW_COLLAPSED": True,
    "JQUERY_URL": "",
    "SHOW_TOOLBAR_CALLBACK": "aleksis.core.util.core_helpers.dt_show_toolbar",
}

ALLOWED_HOSTS = _settings.get("http.allowed_hosts", [])

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sites",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "polymorphic",
    "django_global_request",
    "settings_context_processor",
    "sass_processor",
    "easyaudit",
    "constance",
    "constance.backends.database",
    "django_any_js",
    "django_yarnpkg",
    "django_tables2",
    "easy_thumbnails",
    "image_cropping",
    "maintenance_mode",
    "menu_generator",
    "phonenumber_field",
    "debug_toolbar",
    "django_select2",
    "hattori",
    "templated_email",
    "html2text",
    "django_otp.plugins.otp_totp",
    "django_otp.plugins.otp_static",
    "django_otp",
    "otp_yubikey",
    "aleksis.core",
    "impersonate",
    "two_factor",
    "material",
    "pwa",
    "ckeditor",
    "django_js_reverse",
    "colorfield",
    "django_bleach",
]

merge_app_settings("INSTALLED_APPS", INSTALLED_APPS, True)
INSTALLED_APPS += get_app_packages()

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "django_yarnpkg.finders.NodeModulesFinder",
    "sass_processor.finders.CssFinder",
]

MIDDLEWARE = [
    #    'django.middleware.cache.UpdateCacheMiddleware',
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.http.ConditionalGetMiddleware",
    "django_global_request.middleware.GlobalRequestMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django_otp.middleware.OTPMiddleware",
    "impersonate.middleware.ImpersonateMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "easyaudit.middleware.easyaudit.EasyAuditMiddleware",
    "maintenance_mode.middleware.MaintenanceModeMiddleware",
    #    'django.middleware.cache.FetchFromCacheMiddleware'
]

ROOT_URLCONF = "aleksis.core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "maintenance_mode.context_processors.maintenance_mode",
                "settings_context_processor.context_processors.settings",
                "constance.context_processors.config",
                "aleksis.core.util.core_helpers.custom_information_processor",
            ],
        },
    },
]

THUMBNAIL_PROCESSORS = (
    "image_cropping.thumbnail_processors.crop_corners",
) + thumbnail_settings.THUMBNAIL_PROCESSORS

# Already included by base template / Bootstrap
IMAGE_CROPPING_JQUERY_URL = None

WSGI_APPLICATION = "aleksis.core.wsgi.application"

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": _settings.get("database.name", "aleksis"),
        "USER": _settings.get("database.username", "aleksis"),
        "PASSWORD": _settings.get("database.password", None),
        "HOST": _settings.get("database.host", "127.0.0.1"),
        "PORT": _settings.get("database.port", "5432"),
        "ATOMIC_REQUESTS": True,
    }
}

merge_app_settings("DATABASES", DATABASES, False)

if _settings.get("caching.memcached.enabled", False):
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.memcached.MemcachedCache",
            "LOCATION": _settings.get("caching.memcached.address", "127.0.0.1:11211"),
        }
    }

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]

# Authentication backends are dynamically populated
AUTHENTICATION_BACKENDS = []

if _settings.get("ldap.uri", None):
    # LDAP dependencies are not necessarily installed, so import them here
    import ldap  # noqa
    from django_auth_ldap.config import LDAPSearch, NestedGroupOfNamesType, NestedGroupOfUniqueNamesType, PosixGroupType  # noqa

    # Enable Django's integration to LDAP
    AUTHENTICATION_BACKENDS.append("django_auth_ldap.backend.LDAPBackend")

    AUTH_LDAP_SERVER_URI = _settings.get("ldap.uri")

    # Optional: non-anonymous bind
    if _settings.get("ldap.bind.dn", None):
        AUTH_LDAP_BIND_DN = _settings.get("ldap.bind.dn")
        AUTH_LDAP_BIND_PASSWORD = _settings.get("ldap.bind.password")

    # Search attributes to find users by username
    AUTH_LDAP_USER_SEARCH = LDAPSearch(
        _settings.get("ldap.users.base"),
        ldap.SCOPE_SUBTREE,
        _settings.get("ldap.users.filter", "(uid=%(user)s)"),
    )

    # Mapping of LDAP attributes to Django model fields
    AUTH_LDAP_USER_ATTR_MAP = {
        "first_name": _settings.get("ldap.map.first_name", "givenName"),
        "last_name": _settings.get("ldap.map.last_name", "sn"),
        "email": _settings.get("ldap.map.email", "mail"),
    }

    # Discover flags by LDAP groups
    if _settings.get("ldap.groups.base", None):
        AUTH_LDAP_GROUP_SEARCH = LDAPSearch(
            _settings.get("ldap.groups.base"),
            ldap.SCOPE_SUBTREE,
            _settings.get("ldap.groups.filter", "(objectClass=%s)" % _settings.get("ldap.groups.type", "groupOfNames")),
        )

        _group_type = _settings.get("ldap.groups.type", "groupOfNames").lower()
        if _group_type == "groupofnames":
            AUTH_LDAP_GROUP_TYPE = NestedGroupOfNamesType()
        elif _group_type == "groupofuniquenames":
            AUTH_LDAP_GROUP_TYPE = NestedGroupOfUniqueNamesType()
        elif _group_type == "posixgroup":
            AUTH_LDAP_GROUP_TYPE = PosixGroupType()

        AUTH_LDAP_USER_FLAGS_BY_GROUP = {
        }
        for _flag in ["is_active", "is_staff", "is_superuser"]:
            _dn = _settings.get("ldap.groups.flags.%s" % _flag, None)
            if _dn:
                AUTH_LDAP_USER_FLAGS_BY_GROUP[_flag] = _dn

        # Backend admin requires superusers to also be staff members
        if "is_superuser" in AUTH_LDAP_USER_FLAGS_BY_GROUP and "is_staff" not in AUTH_LDAP_USER_FLAGS_BY_GROUP:
            AUTH_LDAP_USER_FLAGS_BY_GROUP["is_staff"] = AUTH_LDAP_USER_FLAGS_BY_GROUP["is_superuser"]

# Add ModelBckend last so all other backends get a chance
# to verify passwords first
AUTHENTICATION_BACKENDS.append("django.contrib.auth.backends.ModelBackend")

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGES = [
    ("de", _("German")),
    ("en", _("English")),
]
LANGUAGE_CODE = _settings.get("l10n.lang", "en")
TIME_ZONE = _settings.get("l10n.tz", "UTC")
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/


STATIC_URL = _settings.get("static.url", "/static/")
MEDIA_URL = _settings.get("media.url", "/media/")

LOGIN_REDIRECT_URL = "index"
LOGOUT_REDIRECT_URL = "index"

STATIC_ROOT = _settings.get("static.root", os.path.join(BASE_DIR, "static"))
MEDIA_ROOT = _settings.get("media.root", os.path.join(BASE_DIR, "media"))
NODE_MODULES_ROOT = _settings.get("node_modules.root", os.path.join(BASE_DIR, "node_modules"))

YARN_INSTALLED_APPS = [
    "datatables",
    "jquery",
    "materialize-css",
    "material-design-icons-iconfont",
    "select2",
    "paper-css",
]

merge_app_settings("YARN_INSTALLED_APPS", YARN_INSTALLED_APPS, True)

JS_URL = _settings.get("js_assets.url", STATIC_URL)
JS_ROOT = _settings.get("js_assets.root", NODE_MODULES_ROOT + "/node_modules")

SELECT2_CSS = JS_URL + "/select2/dist/css/select2.min.css"
SELECT2_JS = JS_URL + "/select2/dist/js/select2.min.js"
SELECT2_I18N_PATH = JS_URL + "/select2/dist/js/i18n"

ANY_JS = {
    "DataTables": {"js_url": JS_URL + "/datatables/media/js/jquery.dataTables.min.js"},
    "materialize": {"js_url": JS_URL + "/materialize-css/dist/js/materialize.min.js"},
    "jQuery": {"js_url": JS_URL + "/jquery/dist/jquery.min.js"},
    "material-design-icons": {
        "css_url": JS_URL + "/material-design-icons-iconfont/dist/material-design-icons.css"
    },
    "paper-css": {"css_url": JS_URL + "/paper-css/paper.min.css"},
}

merge_app_settings("ANY_JS", ANY_JS, True)

SASS_PROCESSOR_ENABLED = True
SASS_PROCESSOR_AUTO_INCLUDE = False
SASS_PROCESSOR_CUSTOM_FUNCTIONS = {
    "get-colour": "aleksis.core.util.sass_helpers.get_colour",
    "get-config": "aleksis.core.util.sass_helpers.get_config",
}
SASS_PROCESSOR_INCLUDE_DIRS = [
    _settings.get("materialize.sass_path", JS_ROOT + "/materialize-css/sass/"),
    STATIC_ROOT,
]

ADMINS = _settings.get("contact.admins", [])
SERVER_EMAIL = _settings.get("contact.from", "root@localhost")
DEFAULT_FROM_EMAIL = _settings.get("contact.from", "root@localhost")
MANAGERS = _settings.get("contact.admins", [])

if _settings.get("mail.server.host", None):
    EMAIL_HOST = _settings.get("mail.server.host")
    EMAIL_USE_TLS = _settings.get("mail.server.tls", False)
    EMAIL_USE_SSL = _settings.get("mail.server.ssl", False)
    if _settings.get("mail.server.port", None):
        EMAIL_PORT = _settings.get("mail.server.port")
    if _settings.get("mail.server.user", None):
        EMAIL_HOST_USER = _settings.get("mail.server.user")
        EMAIL_HOST_PASSWORD = _settings.get("mail.server.password")

TEMPLATED_EMAIL_BACKEND = 'templated_email.backends.vanilla_django'
TEMPLATED_EMAIL_AUTO_PLAIN = True


TEMPLATE_VISIBLE_SETTINGS = ["ADMINS", "DEBUG"]

CONSTANCE_BACKEND = "constance.backends.database.DatabaseBackend"
CONSTANCE_ADDITIONAL_FIELDS = {
    "char_field": ["django.forms.CharField", {}],
    "image_field": ["django.forms.ImageField", {}],
    "email_field": ["django.forms.EmailField", {}],
    "url_field": ["django.forms.URLField", {}],
    "integer_field": ["django.forms.IntegerField", {}],
    "password_field": ["django.forms.CharField", {
        'widget': 'django.forms.PasswordInput',
    }],
    "adressing-select": ['django.forms.fields.ChoiceField', {
        'widget': 'django.forms.Select',
        'choices': ((None, "-----"),
                    # ("german", _("<first name>") + " " + _("<last name>")),
                    # ("english", _("<last name>") + ", " + _("<first name>")),
                    # ("netherlands", _("<last name>") + " " + _("<first name>")),
                    ("german", "John Doe"),
                    ("english", "Doe, John"),
                    ("dutch", "Doe John"),
                    )
    }],
    "notifications-select": ["django.forms.fields.MultipleChoiceField", {
        "widget": "django.forms.CheckboxSelectMultiple",
        "choices": get_notification_choices_lazy,
    }],
    "weekday_field": ["django.forms.fields.ChoiceField", {
        'widget': 'django.forms.Select',
        "choices":  i18n_day_name_choices_lazy
    }],
    "colour_field": ["django.forms.CharField", {
        "widget": "colorfield.widgets.ColorWidget"
    }],
}
CONSTANCE_CONFIG = {
    "SITE_TITLE": ("AlekSIS", _("Site title"), "char_field"),
    "SITE_DESCRIPTION": ("The Free School Information System", _("Site description")),
    "COLOUR_PRIMARY": ("#0d5eaf", _("Primary colour"), "colour_field"),
    "COLOUR_SECONDARY": ("#0d5eaf", _("Secondary colour"), "colour_field"),
    "MAIL_OUT_NAME": ("AlekSIS", _("Mail out name")),
    "MAIL_OUT": (DEFAULT_FROM_EMAIL, _("Mail out address"), "email_field"),
    "PRIVACY_URL": ("", _("Link to privacy policy"), "url_field"),
    "IMPRINT_URL": ("", _("Link to imprint"), "url_field"),
    "ADRESSING_NAME_FORMAT": ("german", _("Name format of adresses"), "adressing-select"),
    "NOTIFICATION_CHANNELS": (["email"], _("Channels to allow for notifications"), "notifications-select"),
    "PRIMARY_GROUP_PATTERN": ("", _("Regular expression to match primary group, e.g. '^Class .*'"), str),
}
CONSTANCE_CONFIG_FIELDSETS = {
    "General settings": ("SITE_TITLE", "SITE_DESCRIPTION"),
    "Theme settings": ("COLOUR_PRIMARY", "COLOUR_SECONDARY"),
    "Mail settings": ("MAIL_OUT_NAME", "MAIL_OUT"),
    "Notification settings": ("NOTIFICATION_CHANNELS", "ADRESSING_NAME_FORMAT"),
    "Footer settings": ("PRIVACY_URL", "IMPRINT_URL"),
    "Account settings": ("PRIMARY_GROUP_PATTERN",),
}

merge_app_settings("CONSTANCE_ADDITIONAL_FIELDS", CONSTANCE_ADDITIONAL_FIELDS, False)
merge_app_settings("CONSTANCE_CONFIG", CONSTANCE_CONFIG, False)
merge_app_settings("CONSTANCE_CONFIG_FIELDSETS", CONSTANCE_CONFIG_FIELDSETS, False)

MAINTENANCE_MODE = _settings.get("maintenance.enabled", None)
MAINTENANCE_MODE_IGNORE_IP_ADDRESSES = _settings.get(
    "maintenance.ignore_ips", _settings.get("maintenance.internal_ips", [])
)
MAINTENANCE_MODE_GET_CLIENT_IP_ADDRESS = "ipware.ip.get_ip"
MAINTENANCE_MODE_IGNORE_SUPERUSER = True
MAINTENANCE_MODE_STATE_FILE_PATH = _settings.get(
    "maintenance.statefile", "maintenance_mode_state.txt"
)

IMPERSONATE = {"USE_HTTP_REFERER": True, "REQUIRE_SUPERUSER": True, "ALLOW_SUPERUSER": True}

DJANGO_TABLES2_TEMPLATE = "django_tables2/materialize.html"

ANONYMIZE_ENABLED = _settings.get("maintenance.anonymisable", True)

LOGIN_URL = "two_factor:login"

if _settings.get("2fa.call.enabled", False):
    if "two_factor.middleware.threadlocals.ThreadLocals" not in MIDDLEWARE:
        MIDDLEWARE.insert(
            MIDDLEWARE.index("django_otp.middleware.OTPMiddleware") + 1,
            "two_factor.middleware.threadlocals.ThreadLocals",
        )
    TWO_FACTOR_CALL_GATEWAY = "two_factor.gateways.twilio.gateway.Twilio"

if _settings.get("2fa.sms.enabled", False):
    if "two_factor.middleware.threadlocals.ThreadLocals" not in MIDDLEWARE:
        MIDDLEWARE.insert(
            MIDDLEWARE.index("django_otp.middleware.OTPMiddleware") + 1,
            "two_factor.middleware.threadlocals.ThreadLocals",
        )
    TWO_FACTOR_SMS_GATEWAY = "two_factor.gateways.twilio.gateway.Twilio"

if _settings.get("twilio.sid", None):
    TWILIO_SID = _settings.get("twilio.sid")
    TWILIO_TOKEN = _settings.get("twilio.token")
    TWILIO_CALLER_ID = _settings.get("twilio.callerid")

if _settings.get("celery.enabled", False):
    INSTALLED_APPS += ("django_celery_beat", "django_celery_results")
    CELERY_BROKER_URL = "redis://localhost"
    CELERY_RESULT_BACKEND = "django-db"
    CELERY_CACHE_BACKEND = "django-cache"
    CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

    if _settings.get("celery.email", False):
        INSTALLED_APPS += ("djcelery_email",)
        EMAIL_BACKEND = "djcelery_email.backends.CeleryEmailBackend"

PWA_APP_NAME = lazy_config("SITE_TITLE")
PWA_APP_DESCRIPTION = lazy_config("SITE_DESCRIPTION")
PWA_APP_THEME_COLOR = lazy_config("COLOUR_PRIMARY")
PWA_APP_BACKGROUND_COLOR = "#ffffff"
PWA_APP_DISPLAY = "standalone"
PWA_APP_ORIENTATION = "any"
PWA_APP_ICONS = [  # three icons to upload dbsettings
    {"src": STATIC_URL + "/icons/android_192.png", "sizes": "192x192"},
    {"src": STATIC_URL + "/icons/android_512.png", "sizes": "512x512"},
]
PWA_APP_ICONS_APPLE = [
    {"src": STATIC_URL + "/icons/apple_76.png", "sizes": "76x76"},
    {"src": STATIC_URL + "/icons/apple_114.png", "sizes": "114x114"},
    {"src": STATIC_URL + "/icons/apple_152.png", "sizes": "152x152"},
    {"src": STATIC_URL + "/icons/apple_180.png", "sizes": "180x180"},
]
PWA_APP_SPLASH_SCREEN = [
    {
        "src": STATIC_URL + "/icons/android_512.png",
        "media": "(device-width: 320px) and (device-height: 568px) and (-webkit-device-pixel-ratio: 2)",
    }
]
PWA_SERVICE_WORKER_PATH = os.path.join(STATIC_ROOT, "js", "serviceworker.js")

SITE_ID = 1

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar_Basic': [
            ['Source', '-', 'Bold', 'Italic']
        ],
        'toolbar_Full': [
            {'name': 'document', 'items': ['Source', '-', 'Save', 'NewPage', 'Preview', 'Print', '-', 'Templates']},
            {'name': 'clipboard', 'items': ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo']},
            {'name': 'editing', 'items': ['Find', 'Replace', '-', 'SelectAll']},
            {'name': 'insert',
             'items': ['Image', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak', 'Iframe']},
            '/',
            {'name': 'basicstyles',
             'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat']},
            {'name': 'paragraph',
             'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-',
                       'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl',
                       'Language']},
            {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},
            '/',
            {'name': 'styles', 'items': ['Styles', 'Format', 'Font', 'FontSize']},
            {'name': 'colors', 'items': ['TextColor', 'BGColor']},
            {'name': 'tools', 'items': ['Maximize', 'ShowBlocks']},
            {'name': 'about', 'items': ['About']},
            {'name': 'customtools', 'items': [
                'Preview',
                'Maximize',
            ]},
        ],
        'toolbar': 'Full',
        'tabSpaces': 4,
        'extraPlugins': ','.join([
            'uploadimage',
            'div',
            'autolink',
            'autoembed',
            'embedsemantic',
            'autogrow',
            # 'devtools',
            'widget',
            'lineutils',
            'clipboard',
            'dialog',
            'dialogui',
            'elementspath'
        ]),
    }
}

# Which HTML tags are allowed
BLEACH_ALLOWED_TAGS = ['p', 'b', 'i', 'u', 'em', 'strong', 'a', 'div']

# Which HTML attributes are allowed
BLEACH_ALLOWED_ATTRIBUTES = ['href', 'title', 'style']

# Which CSS properties are allowed in 'style' attributes (assuming
# style is an allowed attribute)
BLEACH_ALLOWED_STYLES = [
    'font-family', 'font-weight', 'text-decoration', 'font-variant'
]

# Strip unknown tags if True, replace with HTML escaped characters if
# False
BLEACH_STRIP_TAGS = True

# Strip comments, or leave them in.
BLEACH_STRIP_COMMENTS = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s: %(message)s'
        }
    },
    'root': {
        'handlers': ['console'],
        'level': _settings.get("logging.level", "WARNING"),
        'formatter': "verbose"
    },
}
