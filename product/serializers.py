
from rest_framework import serializers
from wagtail.fields import StreamValue
from .models import ProductPage
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from ecomapp.utils import get_image_rendition
from wagtail.images.models import Image

class ProductPageSerializer(serializers.ModelSerializer):
  
    content = serializers.SerializerMethodField()

    class Meta:
        model = ProductPage
        fields = ['id', 'title', 'content']

    def get_content(self, instance):
        content_data = []
        for block in instance.content:
            if isinstance(block, blocks.StructBlock) and block.block_type == 'product_details':
                details = {
                    'main_title': block.value.get('main_title'),
                    'description': block.value.get('description').source,  
                    'category': block.value.get('category'),
                    'available_size': block.value.get('available_size'),
                    'images': self.get_images(block),
                    'tags': block.value.get('tags'),
                }
                content_data.append(details)
        return content_data
    def get_images(self, block):
        images_data = []
        images = block.value.get('images', [])
        for image_block in images:
            if isinstance(image_block, Image):
                image_data = self.get_image_data(image_block)
                if image_data:
                    images_data.append(image_data)
        return images_data

    def get_image_data(self, image_block):
        if isinstance(image_block, Image):
            rendition = get_image_rendition(image_block, 'original')
            if rendition:
                return {
                    "url": rendition['url'],
                    "title": image_block.title,
                    "width": rendition['width'],
                    "height": rendition['height'],
                    "alt": image_block.default_alt_text,
                }
        return None

    

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if hasattr(instance, 'content') and isinstance(instance.content, StreamValue):
            representation['content'] = self.serialize_streamfield(instance.content)
        return representation

    def serialize_streamfield(self, streamfield):
        if isinstance(streamfield, StreamValue):
            return [self.serialize_block(block) for block in streamfield]
        return []

    def serialize_block(self, block):
        if not hasattr(block, 'value'):
            return {
                'type': 'unknown',
                'value': str(block),
            }

        block_value = block.value
        block_instance = block.block

        if isinstance(block_instance, blocks.RichTextBlock):
            return {
                'type': 'rich_text',
                'content': block_value.source if hasattr(block_value, 'source') else str(block_value),
            }
        elif isinstance(block_instance, ImageChooserBlock):
            image_data = self.get_image_data(block_value)
            return {
                'type': 'image',
                'data': image_data,
            }
        elif isinstance(block_instance, blocks.CharBlock):
            return {
                'type': 'text',
                'text': block_value,
            }
        elif isinstance(block_instance, blocks.StructBlock):
            serialized_data = {key: self.serialize_block(value) for key, value in block_value.items()}
            return {
                'type': 'struct',
                'fields': serialized_data,
            }
        return {
            'type': 'unknown',
            'value': str(block_value),
        }

class ProductPageDetailSerializer(ProductPageSerializer):
    class Meta(ProductPageSerializer.Meta):
        fields = ['id', 'title', 'content']