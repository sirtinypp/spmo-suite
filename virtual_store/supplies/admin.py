from django.contrib import admin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from import_export.admin import ImportExportModelAdmin
from .models import Category, Product, Order, OrderItem, StockBatch
from django.contrib import admin
from .models import AnnualProcurementPlan

# --- 1. PRODUCT RESOURCE (For Master List Upload) ---
class ProductResource(resources.ModelResource):
    category = fields.Field(
        column_name='category',
        attribute='category',
        widget=ForeignKeyWidget(Category, field='name')
    )

    class Meta:
        model = Product
        # This maps the CSV headers to the Database fields
        fields = ('id', 'name', 'item_code', 'brand', 'supplier', 'description', 'price', 'category', 'stock')
        import_id_fields = ('id',)

# --- 2. STOCK BATCH RESOURCE (For Replenishment via Item Code) ---
class StockBatchResource(resources.ModelResource):
    # This tells Django: "Look at the 'item_code' column in the CSV, 
    # search for a Product with that item_code, and link it."
    product = fields.Field(
        column_name='item_code',
        attribute='product',
        widget=ForeignKeyWidget(Product, field='item_code')
    )

    class Meta:
        model = StockBatch
        # These are the headers your CSV MUST have
        fields = ('product', 'supplier_name', 'batch_number', 'quantity_initial', 'cost_per_item', 'date_received')

    def after_save_instance(self, instance, using_transactions, dry_run):
        """
        After the batch is uploaded, automatically update the Main Product's 
        stock level and price.
        """
        if not dry_run:
            try:
                # 1. Get the product linked to this batch
                product_to_update = instance.product
                
                # 2. Add the new quantity
                product_to_update.stock += instance.quantity_initial
                
                # 3. Update the price
                product_to_update.price = instance.cost_per_item
                
                # 4. Save Product changes
                product_to_update.save()

                # 5. Set remaining quantity for FIFO tracking
                instance.quantity_remaining = instance.quantity_initial
                instance.save()
            except Exception as e:
                print(f"Error updating product stock: {e}")

# --- ADMIN REGISTRATIONS ---

@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    list_display = ('name', 'description')

@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    resource_class = ProductResource
    # Shows Item Code, Name, and Brand in the list
    list_display = ('item_code', 'name', 'brand', 'category', 'price', 'stock')
    search_fields = ('name', 'item_code', 'brand') 
    list_filter = ('category', 'brand')

@admin.register(StockBatch)
class StockBatchAdmin(ImportExportModelAdmin):
    resource_class = StockBatchResource
    # Shows Batch info in the list
    list_display = ('get_item_code', 'get_product_name', 'batch_number', 'quantity_remaining', 'date_received')
    list_filter = ('date_received',)
    
    # Helper to show product info in the Batch list
    def get_item_code(self, obj):
        return obj.product.item_code
    get_item_code.short_description = 'Item Code'

    def get_product_name(self, obj):
        return obj.product.name
    get_product_name.short_description = 'Product Name'

admin.site.register(Order)
admin.site.register(OrderItem)

@admin.register(AnnualProcurementPlan)
class APPAdmin(admin.ModelAdmin):
    list_display = ('department', 'product', 'year', 'quantity_approved', 'quantity_consumed', 'remaining_balance')
    list_filter = ('department', 'year')
    search_fields = ('product__name', 'department')
    
    # Optional: Make 'quantity_consumed' read-only so admins don't accidentally edit it manually
    # readonly_fields = ('quantity_consumed',)