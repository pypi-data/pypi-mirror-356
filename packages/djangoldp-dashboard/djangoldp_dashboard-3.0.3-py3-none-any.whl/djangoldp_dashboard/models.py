from django.db import models
from django.db.models import F, Max
from django.utils.translation import gettext_lazy as _
from djangoldp.models import Model
from djangoldp.permissions import ReadOnly

SIZE_CHOICES = [
    ('1', '1'),
    ('12', '1/2'),
    ('13', '1/3'),
    ('14', '1/4'),
    ('23', '2/3'),
    ('24', '2/4'),
    ('34', '3/4')
]

class Dashboard(Model):
    target = models.CharField(max_length=20, default='default')
    order = models.IntegerField(blank=True, null=True)
    size = models.CharField(max_length=2, choices=SIZE_CHOICES, default='1')
    background = models.BooleanField(default=True)
    content = models.TextField()

    def save(self, *args, **kwargs):
        if self.pk is None:
            if self.order is None:
                max_order = Dashboard.objects.filter(target=self.target).aggregate(Max('order'))['order__max']
                self.order = (max_order + 1) if max_order is not None else 1
            else:
                Dashboard.objects.filter(target=self.target, order__gte=self.order).update(order=F('order') + 1)
        else:
            old_order = Dashboard.objects.get(pk=self.pk).order
            if self.order is None:
                max_order = Dashboard.objects.filter(target=self.target).aggregate(Max('order'))['order__max']
                self.order = (max_order + 1) if max_order is not None else 1
            if old_order is not None and self.order is not None and self.order != old_order:
                if self.order > old_order:
                    Dashboard.objects.filter(target=self.target, order__gt=old_order, order__lte=self.order).update(order=F('order') - 1)
                else:
                    Dashboard.objects.filter(target=self.target, order__lt=old_order, order__gte=self.order).update(order=F('order') + 1)

        super(Dashboard, self).save(*args, **kwargs)

    class Meta(Model.Meta):
        verbose_name = _("Dashboard")
        verbose_name_plural = _("Dashboards")
        ordering = ["target"]
        serializer_fields = [
            "@id",
            "target",
            "order",
            "size",
            "background",
            "content",
        ]
        permission_classes = [ReadOnly]
