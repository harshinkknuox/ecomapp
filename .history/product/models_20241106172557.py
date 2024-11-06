from django.db import models
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock
from django.utils.translation import gettext_lazy as _

class ProductPage(Page):
    content = StreamField([
        ('product_details', blocks.StructBlock([
            ('main_title', blocks.CharBlock(help_text="Enter the product title")),
            ('description', blocks.RichTextBlock(help_text="Provide a description of the product")),
            ('category', blocks.PageChooserBlock(required=False, help_text="Select Category page")),
            ('available_size',blocks.ListBlock(blocks.CharBlock( help_text="Enter the price of the product"))),
            ('images',blocks.ListBlock(ImageChooserBlock(help_text="Upload or select an image for the product"))),
            ('tags', blocks.ListBlock(blocks.CharBlock(help_text="Add tags to describe the product"))),
        ])),
    ], use_json_field=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('content'),
    ]
    
    template = "product/product.html"

    class Meta:
        verbose_name = _("Product Page")
        verbose_name_plural = _("Product Pages")
