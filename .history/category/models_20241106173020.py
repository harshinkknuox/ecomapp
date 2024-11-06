from django.db import models
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel

from product.models import ProductPage


class ProductCategory(Page):
    cate_title = models.CharField(max_length=255,blank=True,null=True)
    content_panels = Page.content_panels + [
        FieldPanel("cate_title"),
       
    ]

    parent_page_types = ['home.HomePage']
    subpage_types = ['product.ProductPage']
    
    def __str__(self):
        return self.title