from django.db import models
from django.utils import timezone

class NewsPost(models.Model):
    # Category Options (Value, Readable Name)
    CATEGORY_CHOICES = [
        ('MEMO', 'Memorandum'),
        ('EVENT', 'Event'),
        ('ADVISORY', 'Advisory'),
        ('GFA', 'GFA Update'),
    ]

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='ADVISORY')
    summary = models.TextField(help_text="Short description for the card (Max 200 chars recommended)")
    
    # --- NEW FIELD FOR POPUP CONTENT ---
    content = models.TextField(help_text="The full article content for the popup", blank=True, null=True)
    # -----------------------------------

    # Uploads
    image = models.ImageField(upload_to='news_images/', help_text="Card thumbnail image")
    attachment = models.FileField(upload_to='news_docs/', blank=True, null=True, help_text="Optional: Upload PDF Memo")
    
    date_posted = models.DateTimeField(default=timezone.now)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['-date_posted'] 
        # app_label = 'config' (Not needed since we added 'config' to INSTALLED_APPS)

    def __str__(self):
        return self.title

    # Helper to pick colors based on category
    @property
    def color_theme(self):
        themes = {
            'MEMO': 'blue',
            'EVENT': 'amber',
            'ADVISORY': 'red',
            'GFA': 'emerald'
        }
        return themes.get(self.category, 'slate')