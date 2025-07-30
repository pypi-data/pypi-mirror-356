from zenutils import importutils

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from import_export.admin import ImportExportActionModelAdmin
from import_export.resources import ModelResource
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget

from .models import Warning
from .models import WaringCategory

from .actions import django_site_warnings_acknowledge
from .actions import django_site_warnings_deny

DjangoSiteWarningsBaseAdminName = getattr(
    settings,
    "DJANGO_SITE_WARNINGS_ADMIN_BASE",
    "django.contrib.admin.ModelAdmin",
)
DjangoSiteWarningsBaseAdmin = importutils.import_from_string(
    DjangoSiteWarningsBaseAdminName
)
if not DjangoSiteWarningsBaseAdmin:
    DjangoSiteWarningsBaseAdmin = admin.ModelAdmin


class WaringCategoryAdmin(
    ImportExportActionModelAdmin,
    DjangoSiteWarningsBaseAdmin,
):
    list_display = [
        "name",
        "code",
        "display_order",
    ]
    ordering = [
        "display_order",
    ]
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "name",
                    "code",
                    "display_order",
                ]
            },
        )
    ]


class WarningResource(ModelResource):
    category = Field(
        attribute="category",
        column_name="category",
        widget=ForeignKeyWidget(
            WaringCategory,
            field="name",
        ),
    )

    class Meta:
        model = Warning
        fields = (
            "id",
            "title",
            "category",
            "data",
            "add_time",
            "ack",
            "ack_time",
            "mod_time",
        )


class WarningAdmin(
    ImportExportActionModelAdmin,
    DjangoSiteWarningsBaseAdmin,
):
    resource_classes = [WarningResource]
    ordering = [
        "-id",
    ]
    list_display = [
        "id",
        "title",
        "category",
        "add_time",
        "ack",
    ]
    list_filter = [
        "category",
        "ack",
        "add_time",
    ]
    fieldsets = (
        (
            None,
            {
                "fields": [
                    "title",
                    "category",
                    "data",
                    "ack",
                ],
            },
        ),
        (
            _("Date/Times"),
            {
                "fields": [
                    "add_time",
                    "mod_time",
                    "ack_time",
                ]
            },
        ),
    )
    readonly_fields = [
        "title",
        "category",
        "data",
        "ack",
        "add_time",
        "mod_time",
        "ack_time",
    ]
    actions = [
        django_site_warnings_acknowledge,
        django_site_warnings_deny,
    ]


admin.site.register(WaringCategory, WaringCategoryAdmin)
admin.site.register(Warning, WarningAdmin)
