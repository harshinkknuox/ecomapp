from django.conf import settings
from django.core.cache import cache
from wagtail.images.models import Image
from wagtail.rich_text import RichText
from bs4 import BeautifulSoup

def get_rich_text_content(content, request):   
    if not content:
        return None

    if isinstance(content, RichText):
        content = str(content)

    if not request: 
        return content 

    soup = BeautifulSoup(content, 'html.parser')
    for img_tag in soup.find_all('img'):
        src = img_tag.get('src')
        if src:
            img_tag['src'] = request.build_absolute_uri(src)

    return str(soup)

def get_image_rendition(image, rendition_spec, cache_timeout=3600):
    print("--------------sjdhfsjdhfh-------------")
    if not image:
        print("-------------------------No image ")
        return None
    print(f"Requested rendition_spec: {rendition_spec}")      

    valid_specs = ['original', 'fill-800x600', 'max-800x600']  
    if rendition_spec not in valid_specs:
        #print(f"Invalid rendition_spec: {rendition_spec}")
        return None  

    if image.file.name.endswith('.gif'):
        full_url = settings.BASE_URL + image.file.url
        return {
            "url": full_url,
            "full_url": full_url,
            "width": None,  
            "height": None,
            "alt": image.title
        }

    cache_key = f"image_{image.id}_{rendition_spec}"  
    data = cache.get(cache_key)   
    if not data:  
        try:
            rendition = image.get_rendition(rendition_spec)  
            if not rendition:  
                print(f"Rendition not found -------------------------: {rendition_spec}")
                return None

            full_url = settings.BASE_URL + rendition.url  
            data = {
                "url": full_url,  
                "full_url": full_url,  
                "width": rendition.width,  
                "height": rendition.height,  
                "alt": image.title  
            }
            cache.set(cache_key, data, timeout=cache_timeout) 
        except Exception as e:
            print(f"Error generating image rendition ({rendition_spec}):", e) 
            return None 
    return data  