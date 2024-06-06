from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete, pre_save
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.dispatch import receiver
import os


def get_current_user():
    return get_user_model().objects.get_or_create(username='default')[0]
class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/images/', blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=get_current_user)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            original_slug = self.slug
            queryset = Product.objects.all()
            counter = 1
            while queryset.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

# Usamos o sinal pre_save para verificar se a imagem foi alterada
@receiver(pre_save, sender=Product)
def delete_old_image_on_update(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_image = Product.objects.get(pk=instance.pk).image
    except Product.DoesNotExist:
        return False

    if not old_image:
        return False

    new_image = instance.image
    if not old_image == new_image:
        if os.path.isfile(old_image.path):
            os.remove(old_image.path)

@receiver(pre_delete, sender=Product)
def delete_image_on_delete(sender, instance, **kwargs):
    # Excluir a foto relacionada ao produto se existir
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)