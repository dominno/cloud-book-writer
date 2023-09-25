from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.exceptions import ValidationError


class Section(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, related_name='authored_sections', on_delete=models.CASCADE)
    collaborators = models.ManyToManyField(User, related_name='collaborated_sections', blank=True)
    parent_section = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='nested_sections')
    root = models.BooleanField(default=False)
    content_url = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.root:
            parent = self.parent_section
            while parent is not None:
                if parent.root:
                    raise ValidationError("A root section already exists in the hierarchy.")
                parent = parent.parent_section       
        super().save(*args, **kwargs)

    @property
    def storage_key(self):
        return f"{slugify(self.title)}-{self.id}"

