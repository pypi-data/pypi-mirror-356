from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from django_model_helper.models import WithAddModTimeFields
from django_model_helper.models import WithDisplayOrderFields
from django_safe_fields.fields import SafeCharField
from django_safe_fields.fields import SafeTextField


class WaringCategory(WithDisplayOrderFields):
    code = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_("Warning Category Code"),
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_("Warning Category Name"),
    )

    class Meta:
        verbose_name = _("Warning Category")
        verbose_name_plural = _("Warning Categories")

    def __str__(self):
        return self.name

    @classmethod
    def get(cls, code):
        if isinstance(code, WaringCategory):
            return code
        try:
            return cls.objects.get(code=code)
        except cls.DoesNotExist:
            category = cls()
            category.code = code
            category.name = code
            category.save()
            return category


class Warning(WithAddModTimeFields):
    category = models.ForeignKey(
        WaringCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Warning Category"),
    )
    title = SafeCharField(
        max_length=1024,
        verbose_name=_("Warning Title"),
    )
    data = SafeTextField(
        null=True,
        blank=True,
        verbose_name=_("Warning Data"),
    )
    ack = models.BooleanField(
        default=False,
        verbose_name=_("Acknowledged"),
    )
    ack_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Acknowledged Time"),
    )

    class Meta:
        verbose_name = _("Warning")
        verbose_name_plural = _("Warnings")

    def __str__(self):
        return self.title

    @classmethod
    def make(cls, category, title, data=None, save=False):
        category = WaringCategory.get(category)
        try:
            instance = cls.objects.get(ack=False, category=category, title=title)
            return instance
        except cls.DoesNotExist:
            instance = cls()
            instance.category = category
            instance.title = title
            instance.data = data
            if save:
                instance.save()
            return instance

    @classmethod
    def makemany(cls, category, warnings, save=False):
        warning_instances = []
        for warning in warnings:
            if isinstance(warning, (list, tuple)):
                data = warning[1]  # 注意不能调赋值次序
                warning = warning[0]
            else:
                data = None
            instance = Warning.make(
                category=category,
                title=warning,
                data=data,
                save=save,
            )
            warning_instances.append(instance)
        return warning_instances

    def acknowledge(self, save=True):
        self.ack = True
        self.ack_time = timezone.now()
        if save:
            self.save()

    def deny(self, save=True):
        self.ack = False
        self.ack_time = None
        if save:
            self.save()
