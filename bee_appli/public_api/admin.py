# Third-party imports
from django.contrib import admin


# Local imports
from .models import PublicContact


class PublicContactAdmin(admin.ModelAdmin):
    list_display = ("public_beekeeper_info",)
    list_filter = ("public_beekeeper_info",)
    search_fields = ("public_beekeeper_info",)


admin.site.register(PublicContact, PublicContactAdmin)
