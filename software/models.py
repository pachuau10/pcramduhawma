from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


def validate_software_file(value):
    allowed = [e.strip().lower().lstrip('.') for e in getattr(settings, 'ALLOWED_SOFTWARE_EXTENSIONS', []) if e.strip()]
    name = (value.name or '').lower()
    if name.endswith('.tar.gz'):
        ext = 'tar.gz'
    else:
        ext = name.rsplit('.', 1)[-1] if '.' in name else ''
    if allowed and ext not in allowed:
        raise ValidationError(f'File type ".{ext}" is not allowed. Allowed: {", ".join(allowed)}.')
    max_size = getattr(settings, 'MAX_UPLOAD_SIZE', 100 * 1024 * 1024)
    if getattr(value, 'size', 0) and value.size > max_size:
        raise ValidationError(f'File too large ({value.size // (1024 * 1024)} MB). Max is {max_size // (1024 * 1024)} MB.')


class Software(models.Model):
    PLATFORM_CHOICES = [
        ('windows', 'Windows'),
        ('macos', 'macOS'),
        ('linux', 'Linux'),
        ('android', 'Android'),
        ('ios', 'iOS'),
        ('cross_platform', 'Cross Platform'),
        ('web', 'Web'),
        ('other', 'Other'),
    ]

    ARCHITECTURE_CHOICES = [
        ('x86', 'x86'),
        ('x64', 'x64'),
        ('arm', 'ARM'),
        ('arm64', 'ARM64'),
        ('universal', 'Universal'),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    short_description = models.CharField(max_length=300, blank=True, default="")
    version = models.CharField(max_length=50, default="1.0.0")
    release_date = models.DateField()
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES, default='windows')
    architecture = models.CharField(max_length=20, choices=ARCHITECTURE_CHOICES, default='x64')
    file = models.FileField(upload_to='software/', validators=[validate_software_file])
    file_size = models.PositiveIntegerField(help_text="File size in bytes", default=0)
    download_count = models.PositiveIntegerField(default=0)
    features = models.TextField(blank=True, default="", help_text="One feature per line")
    requirements = models.TextField(blank=True, default="")
    installation = models.TextField(blank=True, default="")
    changelog = models.TextField(blank=True, default="")
    source_url = models.URLField(blank=True, default="")
    website_url = models.URLField(blank=True, default="")
    license = models.CharField(max_length=100, blank=True, default="Proprietary")
    featured = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Software"
        verbose_name_plural = "Software"
        ordering = ['-release_date']

    def __str__(self):
        return f"{self.name} v{self.version}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if self.file and not self.file_size:
            try:
                self.file_size = self.file.size
            except (OSError, ValueError):
                pass
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('software:software_detail', kwargs={'slug': self.slug})

    @property
    def file_size_display(self):
        if self.file_size == 0:
            return "Unknown"
        size = self.file_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"

    @property
    def file_extension(self):
        if self.file:
            return self.file.name.split('.')[-1].upper()
        return ""

    def increment_download(self):
        self.download_count += 1
        self.save(update_fields=['download_count'])


class SoftwareScreenshot(models.Model):
    software = models.ForeignKey(Software, on_delete=models.CASCADE, related_name='screenshots')
    image = models.ImageField(upload_to='software/screenshots/')
    caption = models.CharField(max_length=200, blank=True, default="")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.software.name} - Screenshot {self.order}"
