# django-site-warnings

Django application allow to create site warnings, make subscription, and receive notifies.

## Install

```
pip install django-site-warnings
```

## Usage

*pro/views.py*

```python
from django_site_warnings.models import WaringCategory
from django_site_warnings.models import Warning

def background_sync_work(request):
    try:
        pass # do your own work
    except Exception as error:
        category = WaringCategory.get("warning category code")
        Warning.make(category, f"background_sync_work failed: {error}")
```

*pro/settings*

```python
INSTALLED_APPS = [
    '...',
    'django_site_warnings',
    '...',
]

# work together with django-admin-global-sidebar
DJANGO_ADMIN_GLOBAL_SIDEBAR_MENUS = "pro.menus.site_menu"

DJANGO_SITE_WARNING_SITE_NAME = "Site Warning"

# sendmail_notify settings
DJANGO_SITE_WARNING_NOTIFY_MAIL_FROM = "sender@example.com"
DJANGO_SITE_WARNING_NOTIFY_MAIL_TO = ["receiver@example.com"]
DJANGO_SITE_WARNING_NOTIFY_MAIL_SERVER = "smtp.example.com"
DJANGO_SITE_WARNING_NOTIFY_MAIL_PORT = 465
DJANGO_SITE_WARNING_NOTIFY_MAIL_SSL = True
DJANGO_SITE_WARNING_NOTIFY_MAIL_USER = "sender@example.com"
DJANGO_SITE_WARNING_NOTIFY_MAIL_PASSWORD = "sender-password-MlPzC9kt"

# use `DJANGO_SITE_WARNING_NOTIFY_MAIL_CONFIG` to replace the configs above.
# `DJANGO_SITE_WARNING_NOTIFY_MAIL_CONFIG` can also be a string path of a function that returns server info
DJANGO_SITE_WARNING_NOTIFY_MAIL_CONFIG = {
    "from_address": "sender@example.com",
    "to_addresses": ["receiver@example.com"],
    "server": "smtp.example.com",
    "port": 465,
    "ssl": True,
    "user": "sender@example.com",
    "password": "sender-password-MlPzC9kt",
}

```

*`DJANGO_SITE_WARNING_NOTIFY_MAIL_CONFIG` callback function should define as:*

```python
def get_notify_mail_config(warning, payload, force):
    return {
        "from_address": "sender@example.com",
        "to_addresses": ["receiver@example.com"],
        "server": "smtp.example.com",
        "port": 465,
        "ssl": True,
        "user": "sender@example.com",
        "password": "sender-password-MlPzC9kt",
    }
```

*pro/menus.py*

```python
from django_site_warnings.global_sidebar import django_site_warnings_menu_item_of_applist

def site_menu(request=None):
    return [
        {
            "title": _("Home"),
            "icon": "fa fa-home",
            "url": "/admin/",
        },
        {
            "title": _("System Settings"),
            "icon": "fas fa-cogs",
            "children": [
                {
                    "title": _("User Manage"),
                    "icon": "fas fa-user",
                    "model": "auth.user",
                    "permissions": ["auth.view_user"],
                },
                {
                    "title": _("Group Manage"),
                    "icon": "fas fa-users",
                    "model": "auth.group",
                    "permissions": ["auth.view_group"],
                },
                django_site_warnings_menu_item_of_applist,
            ]
        }
    ]
```

## Releases

### v0.1.2

- First release.

### v0.1.4

- Make title length longer. 

### v0.1.6

- Test for Django 3.2.
- Work with django-simpletask2.

### v0.2.0

- Add django_site_warnings.global_sidebar.django_site_warnings_menu_item_of_warning, django_site_warnings.global_sidebar.django_site_warnigns_menu_item_of_category and django_site_warnings.global_sidebar.django_site_warnings_menu_item_of_applist to work with django-admin-global-sidebar.
- WaringCategory.get will auto create category instance if it is missing.
- Register sendmail_notify to Warning by default.

### v0.2.1

- Show notify send result.

### v0.2.2

- Doc update.

### v0.3.7

- Add `DJANGO_SITE_WARNING_NOTIFY_MAIL_CONFIG` support.
- No django-site-warning-server anymore.

### v0.4.0

- 简化告警管理：移除邮件发送相关功能。
