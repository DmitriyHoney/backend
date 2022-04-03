import io
import os.path
from PIL import Image
from django.core.files.base import ContentFile
# from django.shortcuts import get_object_or_404


def create_image_thumb(instance, image_field, thmb_field, width=250):
    """
    create middle photo
    """
    try:
        img = Image.open(image_field)
        w, h = img.size
        new_height = int(width * h / w)
        img.thumbnail((width, new_height), Image.ANTIALIAS)

        thumb_name, thumb_extension = os.path.splitext(image_field.name)
        thumb_extension = thumb_extension.lower()
        thumb_filename = thumb_name + '_thumb' + thumb_extension

        if thumb_extension in ['.jpg', '.jpeg']:
            FTYPE = 'JPEG'
        elif thumb_extension == '.gif':
            FTYPE = 'GIF'
        elif thumb_extension == '.png':
            FTYPE = 'PNG'
        else:
            return False

        temp_thumb = io.BytesIO()
        img.save(temp_thumb, FTYPE)
        temp_thumb.seek(0)

        thmb_field.save(thumb_filename, ContentFile(temp_thumb.read()), save=True)
        temp_thumb.close()

        return True
    except Exception as e:
        print(f'create_image_thumbs error: {str(e)}')
