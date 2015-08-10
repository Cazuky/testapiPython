from tastypie.resources import ModelResource
from api.models import Customer, Product

class CustomerResource(ModelResource):
	class Meta:
		queryset = Customer.objects.all()
		allowed_methods = ['get']

class ProductResource(ModelResource):
	class Meta:
		queryset = Product.objects.all()
		allowed_method = ['get']
