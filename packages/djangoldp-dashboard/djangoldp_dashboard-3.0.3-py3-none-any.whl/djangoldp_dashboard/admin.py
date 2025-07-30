from django.contrib import admin
from djangoldp.admin import DjangoLDPAdmin
from djangoldp.models import Model

from .models import Dashboard


@admin.register(Dashboard)
class DashboardAdmin(DjangoLDPAdmin):
    list_display = ('urlid', 'target', 'order', 'size', 'background')
    exclude = ('urlid', 'is_backlink', 'allow_create_backlink')
    search_fields = ['urlid', 'target', 'order', 'size', 'background', 'content']
    ordering = ['urlid']

    def get_queryset(self, request):
        # Hide distant dashboard cards
        queryset = super(DashboardAdmin, self).get_queryset(request)
        internal_ids = [x.pk for x in queryset if not Model.is_external(x)]
        return queryset.filter(pk__in=internal_ids)
