from django.db import models
from django.db.models.fields.related import ForeignKey
from django.contrib.auth.models import User

# Create your models here.
PRODUCT_CATEGORY = (
    ('M', 'MOBILE'),
    ('C', 'CLOTHES'),
    ('H', 'HOME'),
    ('E', 'ELECTRONIC'),
)

STATE_CHOICES = (
    ('AP' , 'Andhra Pradesh'),
    ('AR' , 'Arunachal Pradesh'),
    ('AS' , 'Assam'),
    ('BR' , 'Bihar'),
    ('CT' , 'Chhattisgarh'),
    ('GA' , 'Goa'),
    ('GJ' , 'Gujarat'),
    ('HR' , 'Haryana'),
    ('HP' , 'Himachal Pradesh'),
    ('JK' , 'Jammu and Kashmir'),
    ('JH' , 'Jharkhand'),
    ('KA' , 'Karnataka'),
    ('KL' , 'Kerala'),
    ('MP' , 'Madhya Pradesh'),
    ('MH' , 'Maharashtra'),
    ('MN' , 'Manipur'),
    ('ML' , 'Meghalaya'),
    ('MZ' , 'Mizoram'),
    ('NL' , 'Nagaland'),
    ('OR' , 'Odisha'),
    ('PB' , 'Punjab'),
    ('RJ' , 'Rajasthan'),
    ('SK' , 'Sikkim'),
    ('TN' , 'Tamil Nadu'),
    ('TG' , 'Telangana'),
    ('TR' , 'Tripura'),
    ('UT' , 'Uttarakhand'),
    ('UP' , 'Uttar Pradesh'),
    ('WB' , 'West Bengal'),
    ('AN' , 'Andaman and Nicobar Islands'),
    ('CH' , 'Chandigarh'),
    ('DN' , 'Dadra and Nagar Haveli'),
    ('DD' , 'Daman and Diu'),
    ('DL' , 'Delhi'),
    ('LD' , 'Lakshadweep'),
    ('PY' , 'Puducherry'),
)

ORDER_CHOICES = (
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
)


class ProductModel(models.Model):
    product_category = models.CharField(max_length=10, choices=PRODUCT_CATEGORY)
    product_brand = models.CharField(max_length=20)
    title = models.CharField(max_length=50)
    desc = models.TextField()
    market_price = models.IntegerField()
    selling_price = models.IntegerField()
    img = models.ImageField('Image1', upload_to="media")

class CustomerModel(models.Model):
    user = ForeignKey(User, on_delete=models.CASCADE)
    name= models.CharField("Full Name", max_length=50)
    mobile = models.IntegerField()
    house_number = models.PositiveIntegerField()
    street = models.CharField('Street/Village', max_length=50)
    locality = models.CharField(max_length=50, blank=True)
    district = models.CharField(max_length=40)
    state = models.CharField(max_length=2, choices=STATE_CHOICES)
    pincode = models.PositiveIntegerField()


class CartModel(models.Model):
    user = ForeignKey(User, on_delete=models.CASCADE)
    product = ForeignKey(ProductModel, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def totalcost(self):
        return self.quantity * self.product.selling_price
    
class Order(models.Model):
    user = ForeignKey(User, on_delete=models.CASCADE)
    customer = ForeignKey(CustomerModel, on_delete=models.CASCADE, null=True)
    product = ForeignKey(ProductModel, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=ORDER_CHOICES, default='Pending')


    @property
    def total_cost(self):
        return self.quantity * self.product.selling_price

