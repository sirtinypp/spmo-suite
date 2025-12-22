from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    def __str__(self): return self.name
    class Meta: verbose_name_plural = "Categories"

class Product(models.Model):
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=100, blank=True, null=True)
    item_code = models.CharField(max_length=50, blank=True, null=True)
    supplier = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    stock = models.IntegerField(default=0)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.name

class StockBatch(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='batches')
    supplier_name = models.CharField(max_length=100, blank=True)
    batch_number = models.CharField(max_length=50, blank=True)
    quantity_initial = models.IntegerField()
    quantity_remaining = models.IntegerField()
    cost_per_item = models.DecimalField(max_digits=10, decimal_places=2)
    date_received = models.DateField(default=timezone.now)
    class Meta: ordering = ['date_received', 'id']
    def __str__(self): return f"{self.product.name} - Batch {self.batch_number}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    employee_name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    remarks = models.TextField(blank=True, null=True)
    
    # --- TIMESTAMPS FOR LEAD TIME MONITORING ---
    created_at = models.DateTimeField(auto_now_add=True) # Request Time
    approved_at = models.DateTimeField(null=True, blank=True) # Approval Time
    completed_at = models.DateTimeField(null=True, blank=True) # Pickup/Delivery Time
    
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Ready for Pickup/Delivery'),
            ('returned', 'Returned to Sender'),
            ('delivered', 'Completed/Delivered'),
        ],
        default='pending'
    )
    document1 = models.FileField(upload_to='order_documents/', blank=True, null=True)
    document2 = models.FileField(upload_to='order_documents/', blank=True, null=True)
    document3 = models.FileField(upload_to='order_documents/', blank=True, null=True)
    def __str__(self): return f"Order #{self.id} - {self.employee_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self): return f"{self.quantity}x {self.product.name}"

    # --- NEW APP MODULE MODELS ---

# ... existing imports ...

class AnnualProcurementPlan(models.Model):
    department = models.CharField(max_length=100, help_text="e.g., HR, IT, Accounting") 
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    year = models.IntegerField(default=2025)
    
    # --- MONTHLY ALLOCATIONS ---
    jan = models.PositiveIntegerField(default=0, verbose_name="Jan")
    feb = models.PositiveIntegerField(default=0, verbose_name="Feb")
    mar = models.PositiveIntegerField(default=0, verbose_name="Mar")
    apr = models.PositiveIntegerField(default=0, verbose_name="Apr")
    may = models.PositiveIntegerField(default=0, verbose_name="May")
    jun = models.PositiveIntegerField(default=0, verbose_name="Jun")
    jul = models.PositiveIntegerField(default=0, verbose_name="Jul")
    aug = models.PositiveIntegerField(default=0, verbose_name="Aug")
    sep = models.PositiveIntegerField(default=0, verbose_name="Sep")
    oct = models.PositiveIntegerField(default=0, verbose_name="Oct")
    nov = models.PositiveIntegerField(default=0, verbose_name="Nov")
    dec = models.PositiveIntegerField(default=0, verbose_name="Dec")

    # The Tracker
    quantity_consumed = models.PositiveIntegerField(default=0, help_text="Quantity already ordered/released")

    class Meta:
        unique_together = ('department', 'product', 'year') 
        verbose_name = "APP Allocation"

    @property
    def quantity_approved(self):
        """Calculates total approved based on monthly inputs"""
        return (
            self.jan + self.feb + self.mar + self.apr + 
            self.may + self.jun + self.jul + self.aug + 
            self.sep + self.oct + self.nov + self.dec
        )

    def remaining_balance(self):
        return self.quantity_approved - self.quantity_consumed

    def __str__(self):
        return f"{self.department} | {self.product.name} | {self.year}"