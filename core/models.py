from django.db import models
from django.core.files.storage import default_storage


class SiteSettings(models.Model):
    site_name = models.CharField(max_length=200, default="PC Ramduhawma's Homepage")
    tagline = models.CharField(max_length=300, default="Thoughts. Code. Life.")
    welcome_message = models.TextField(default="Welcome to my corner of the internet!")
    about_text = models.TextField(blank=True, default="")
    footer_message = models.CharField(max_length=500, default="Thanks for visiting!")
    profile_image = models.ImageField(upload_to='profile/', blank=True, null=True)
    favicon = models.ImageField(upload_to='favicon/', blank=True, null=True)
    og_image = models.ImageField(upload_to='seo/', blank=True, null=True, help_text="Social share image (1200x630). Used for Open Graph and Twitter cards.")
    email = models.EmailField(blank=True, default="")
    github_url = models.URLField(blank=True, default="")
    twitter_url = models.URLField(blank=True, default="")
    discord_url = models.URLField(blank=True, default="")
    facebook_url = models.URLField(blank=True, default="")
    instagram_url = models.URLField(blank=True, default="")
    youtube_url = models.URLField(blank=True, default="")
    linkedin_url = models.URLField(blank=True, default="")
    created_date = models.DateField(auto_now_add=True)
    meta_description = models.CharField(max_length=300, blank=True, default="")
    analytics_code = models.TextField(blank=True, default="")

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        if not self.pk and SiteSettings.objects.exists():
            raise ValueError("Only one SiteSettings instance allowed.")
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class VisitorLog(models.Model):
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True, default="")
    path = models.CharField(max_length=500, blank=True, default="")
    referer = models.URLField(blank=True, default="")
    session_key = models.CharField(max_length=100, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Visitor Log"
        verbose_name_plural = "Visitor Logs"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.ip_address} - {self.path}"


class VisitorCount(models.Model):
    total_visits = models.PositiveIntegerField(default=0)
    unique_visitors = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Visitor Count"
        verbose_name_plural = "Visitor Count"

    def __str__(self):
        return f"Visits: {self.total_visits}, Unique: {self.unique_visitors}"

    def save(self, *args, **kwargs):
        if not self.pk and VisitorCount.objects.exists():
            raise ValueError("Only one VisitorCount instance allowed.")
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class Link(models.Model):
    CATEGORY_CHOICES = [
        ('webring', 'Webring'),
        ('friend', 'Friend'),
        ('resource', 'Resource'),
        ('tool', 'Tool'),
        ('other', 'Other'),
    ]
    name = models.CharField(max_length=200)
    url = models.URLField()
    description = models.TextField(blank=True, default="")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    icon = models.CharField(max_length=50, blank=True, default="")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200, blank=True, default="")
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"

    def __str__(self):
        return f"{self.name} - {self.subject or 'No subject'}"


class NavigationItem(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=500)
    icon = models.CharField(max_length=50, blank=True, default="")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    open_in_new_tab = models.BooleanField(default=False)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Navigation Item"
        verbose_name_plural = "Navigation Items"

    def __str__(self):
        return self.name
