from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


def validate_image(image):
    file_size = image.file.size
    limit_mb = 1
    if file_size > limit_mb * 1024 * 1024:
        raise ValidationError("Max size of file is %s MB" % limit_mb)


class User(AbstractUser):
    GENDER = (
        (True, 'Male'),
        (False, 'Female'),
    )
    user_id = models.AutoField("User ID", primary_key=True, auto_created=True)
    avatar = models.ImageField("User Avatar", null=True, blank=True, upload_to='avatar',
                               validators=[validate_image])
    gender = models.BooleanField("Gender", choices=GENDER, default=True)
    phone_no = models.CharField("Contact No. ", null=False, max_length=12)
    address = models.TextField("Address", null=False, max_length=350)
    State = models.CharField("State ", null=False, max_length=50)
    City = models.CharField("City", null=False, max_length=50)
    pin_code = models.CharField("Zip Code", null=False, max_length=8)

    class Meta:
        ordering = ['username', ]
        verbose_name = 'User'

    @property
    def get_name(self):
        return self.first_name + " " + self.last_name

    @property
    def get_instance(self):
        return self

    def __str__(self):
        return self.username


class Category(models.Model):
    category_name = models.CharField("Category", null=False, max_length=200)
    category_img = models.ImageField("Category Image", null=True, blank=True, upload_to='category',
                                     validators=[validate_image])
    slug = models.SlugField("Slug ", null=False, editable=False, unique=True)

    class Meta:
        ordering = ['category_name', ]
        verbose_name = 'Category'

    def __str__(self):
        return "{}".format(
            self.category_name)


class SubCategory(models.Model):
    sub_category_name = models.CharField("Sub Category", null=False, max_length=200)
    sub_category_img = models.ImageField("Sub Category Image", null=True, blank=True, upload_to='sub_category',
                                         validators=[validate_image])
    slug = models.SlugField("Slug ", null=False, unique=True, editable=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Category (FK)")

    class Meta:
        ordering = ['sub_category_name', ]
        verbose_name = 'Sub Category'

    def __str__(self):
        return "{}".format(
            self.sub_category_name)


class Product(models.Model):
    prod_name = models.CharField("Product Name", max_length=50, null=False)
    prod_desc = models.CharField("Product Description", max_length=2000, null=False)
    prod_price = models.DecimalField("Product Price/Piece", decimal_places=2, default=0.00, max_digits=8)
    prod_img = models.ImageField("Product Image", null=True, blank=True, upload_to='product',
                                 validators=[validate_image])
    q_o_h = models.PositiveIntegerField("Quantity On Hand", null=False, default=0)
    slug = models.SlugField("Slug ", null=False, editable=False, unique=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, verbose_name="Sub Category (FK)")

    class Meta:
        ordering = ['prod_name', ]
        verbose_name = 'Product'

    def __str__(self):
        return "{}".format(
            self.prod_name)


class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Product (FK)")
    prod_img = models.ImageField("Product Image", null=True, blank=True, upload_to='product_img',
                                 validators=[validate_image])

    def __str__(self):
        return "{}".format(
            self.product.prod_name)


class Size(models.Model):
    size = models.CharField("Product Size", max_length=30)

    def __str__(self):
        return "{}".format(
            self.size)


class SizeProductMAp(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Product (FK)")
    size = models.ForeignKey(Size, on_delete=models.CASCADE, verbose_name="Size (FK)")

    def __str__(self):
        return "{} in {} size".format(
            self.product.prod_name, self.size.size)


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Product (FK)")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User (FK)")
    rating = models.PositiveSmallIntegerField("Rating ", validators=[MinValueValidator(0),
                                                                     MaxValueValidator(5)])
    review = models.TextField("Review ", null=True, max_length=300)
    date = models.DateField("Date", null=False, auto_now_add=True)

    def __str__(self):
        return "For {} By {} on {}".format(
            self.product.prod_name, self.user.get_name, self.date)


class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Product (FK)")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User (FK)")
    size = models.CharField("Size", max_length=10, null=False)
    quantity = models.PositiveSmallIntegerField("Quantity ", validators=[MinValueValidator(1),
                                                                         MaxValueValidator(50)], default=1)
    item_total = models.DecimalField("Total Per Item", null=False, decimal_places=2, max_digits=8)

    def __str__(self):
        return "For {} By {} for quantity {}".format(
            self.product.prod_name, self.user.get_name, self.quantity)


class Order(models.Model):
    Order_Status = (
        ("P", 'Paid'),
        ("U", 'Unpaid'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User (FK)", null=False)
    order_amount = models.DecimalField("Total Order Amount", decimal_places=2, max_digits=8)
    order_status = models.CharField("Order Status", choices=Order_Status, max_length=20, default="U")
    phone_no = models.CharField("Contact No. ", null=False, max_length=12)
    address = models.TextField("Address", null=False, max_length=350)
    State = models.CharField("State ", null=False, max_length=50)
    City = models.CharField("City", null=False, max_length=50)
    pin_code = models.CharField("Zip Code", null=False, max_length=8)
    created_at = models.DateTimeField("Order Creation Date Time", null=False, auto_now_add=True)
    note = models.TextField("Note", null=True, max_length=350)

    def __str__(self):
        return "By {} on {}".format(
            self.user.get_name, self.created_at)


class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Order (FK)")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Product (FK)")
    size = models.CharField("Size", max_length=10, null=False)
    quantity = models.PositiveSmallIntegerField("Quantity ", validators=[MinValueValidator(1),
                                                                         MaxValueValidator(50)], default=1)
    item_total = models.DecimalField("Total Per Item", null=False, decimal_places=2, max_digits=8)

    def __str__(self):
        return "For {} Quantity {}".format(
            self.product.prod_name, self.quantity)


class Payment(models.Model):
    Pay_Status = (
        ("P", 'Paid'),
        ("U", 'Unpaid'),
    )
    pay_date = models.DateTimeField("Payment Date", auto_now_add=True, null=False)
    pay_status = models.CharField("Payment Status", choices=Pay_Status, max_length=20, default="U")
    pay_info = models.CharField("Payment Info", max_length=300, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Order (FK)")


class ContactUs(models.Model):
    first_name = models.CharField("First Name", max_length=50, null=False)
    last_name = models.CharField("Last Name", max_length=50, null=False)
    email = models.EmailField("Email", max_length=70, null=False)
    phone = models.CharField("Contact No.", max_length=12, null=False)
    subject = models.CharField("Message Title", max_length=80)
    message = models.TextField("Message", max_length=300, null=False)