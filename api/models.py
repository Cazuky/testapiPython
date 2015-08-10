# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'category'


class Customer(models.Model):
    name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    phone = models.CharField(max_length=45)
    address = models.CharField(max_length=45)
    city_region = models.CharField(max_length=2)
    cc_number = models.CharField(max_length=19)

    class Meta:
        managed = False
        db_table = 'customer'


class CustomerOrder(models.Model):
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    date_created = models.DateTimeField()
    confirmation_number = models.IntegerField()
    customer = models.ForeignKey(Customer)

    class Meta:
        managed = False
        db_table = 'customer_order'


class OrderedProduct(models.Model):
    customer_order = models.ForeignKey(CustomerOrder)
    product = models.ForeignKey('Product')
    quantity = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'ordered_product'
        #unique_together = (('customer_order_id', 'product_id'),)


class Product(models.Model):
    name = models.CharField(max_length=45)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    last_update = models.DateTimeField()
    category = models.ForeignKey(Category)

    class Meta:
        managed = False
        db_table = 'product'
