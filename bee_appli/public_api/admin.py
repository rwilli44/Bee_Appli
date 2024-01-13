# Third-party imports
from django.contrib import admin

# Local imports
from .models import PublicContact


class PublicContactAdmin(admin.ModelAdmin):
    """Class for adding a panel in admin for tracking which beekepers
    have made their contact information public."""

    list_display = ("public_beekeeper_info",)
    list_filter = ("public_beekeeper_info",)
    search_fields = ("public_beekeeper_info",)


admin.site.register(PublicContact, PublicContactAdmin)
