from tastypie.resources import ModelResource
from api.models import Customer, Product
from .corsresource import CorsResourceBase

class CustomerResource(CorsResourceBase, ModelResource):
	class Meta:
		queryset = Customer.objects.all()
		allowed_methods = ['get']

class ProductResource(CorsResourceBase, ModelResource):
	class Meta:
		queryset = Product.objects.all()
		allowed_method = ['get']
