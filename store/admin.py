from django.contrib import admin, messages
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html
from .models import *


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "product_count", "last_update", "created_at"]
    list_display_links = ["id"]
    # list_editable = ["title"]
    search_fields =  ["title"]

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(product_count=Count("product"))

    @admin.display(ordering="product_count")
    def product_count(self, collection):
        #              admin:APP_MODEL_PAGE
        url = reverse("admin:store_product_changelist") + f"?collection={collection.id}"
        # return f"<a href='{url}'>{collection.product_count}</a>"
        return format_html("<a href='{}'>{}</a>", url, collection.product_count)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "price", "inventory", "collection", "inventory_status", "last_update", "created_at"]
    list_display_links = ["id"]
    list_editable = ["price", "inventory"]
    search_fields = ["id", "collection", "title"]
    actions = ["clear_inventory"]
    list_select_related = ["collection"]
    list_per_page: int = 10
    list_max_show_all: int = 500
    
    # create form
    fields = ["title", "product_image", "slug", "description", "price", "inventory", "collection"] 
    exclude = ["promotion"]
    # readonly_fields = ["inventory"]
    prepopulated_fields = {
        "slug": ["title"]
    }
    search_fields = ["collection"]
    autocomplete_fields = ["collection"]


    @admin.action(description="clear inventory")
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request, 
            f"{updated_count} products has been successfully updated.",
            messages.SUCCESS
        )

    @admin.display(ordering="inventory")
    def inventory_status(self, product: Product):
        return "LOW" if product.inventory < 10 else "HIGH"

    def my_collection_id(self, product: Product):
        return product.collection.id
