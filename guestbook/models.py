from django.db import models
from django.utils.html import escape
import re


class GuestbookEntry(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, default="")
    website = models.URLField(blank=True, default="")
    message = models.TextField()
    is_approved = models.BooleanField(default=False)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Guestbook Entry"
        verbose_name_plural = "Guestbook Entries"

    def __str__(self):
        return f"{self.name} - {self.created_at.strftime('%Y-%m-%d')}"

    def save(self, *args, **kwargs):
        self.message = escape(self.message)
        self.name = escape(self.name)
        if self.website:
            if not self.website.startswith(('http://', 'https://')):
                self.website = 'http://' + self.website
        super().save(*args, **kwargs)
