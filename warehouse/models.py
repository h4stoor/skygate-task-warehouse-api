from django.db import models
from django.core.validators import MaxValueValidator

from .const import *


class Product(models.Model):
    name      = models.CharField(max_length=50, unique=True)
    quantity  = models.PositiveSmallIntegerField(default=0)
    
    class Meta:
        verbose_name = 'product'
        
    def __str__(self):
        return self.name
    
    def get_storage(self):
        return self.quantity
        
    @classmethod
    def empty_product(cls):
        try:
            empty_product = cls.objects.get(name='EMPTY')
        except cls.DoesNotExist:
            empty_product = cls.objects.create(name='EMPTY')
        
        return empty_product


class ShelfBox(models.Model):
    product = models.ForeignKey(Product, blank=True, null=True)
    quantity = models.PositiveSmallIntegerField(default=0)
    
    def save(self, *args, **kwargs):
        if not self.product:
            self.product = Product.empty_product()
        if self.quantity and self.quantity > BOX_QUANTITY_MAX_VALUE:
            raise ValueError('quantity value cannot be greater than {}.'.format(BOX_QUANTITY_MAX_VALUE))
        super(ShelfBox, self).save(*args, **kwargs)
    
    @classmethod
    def create_empty_box(cls):
        return cls.objects.create()


class Shelf(models.Model):
    box1 = models.OneToOneField(ShelfBox, related_name='box1')
    box2 = models.OneToOneField(ShelfBox, related_name='box2')
    box3 = models.OneToOneField(ShelfBox, related_name='box3')
    
    class Meta:
        verbose_name = 'shelf'
    
    def get_free_space(self):
        return SHELF_QUANTITY_MAX_VALUE - sum(
            box.quantity for box in [self.box1, self.box2, self.box3]
            )
    
    def get_free_box(self):
        for box in [self.box1, self.box2, self.box3]:
            if box.product.name == 'EMPTY':
                return box
        else:
            return False

    def save(self, *args, **kwargs):
        for field in [self.box1, self.box2, self.box3]:
            if not field:
                field = ShelfBox.create_empty_box()
        super(Shelf, self).save(*args, **kwargs)


class Transport(models.Model):
    STATUS_CHOICES = (
        ('incoming', 'incoming transport'),
        ('waiting', 'waiting for loading'),
        ('loading', 'loading in progress'),
        ('done', 'done'),
    )
    
    product_request = models.CharField(max_length=50)
    cargo = models.PositiveSmallIntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='incoming')
    
    class Meta:
        verbose_name = 'transport'
    
    def __str__(self):
        return self.product_request

    def save(self, *args, **kwargs):
        if self.cargo > CARGO_MAX_VALUE:
            raise ValueError('cargo value cannot be greater than {}.'.format(CARGO_MAX_VALUE))
        super(Transport, self).save(*args, **kwargs)


class DailyTransportsRaport(models.Model):
    pass
