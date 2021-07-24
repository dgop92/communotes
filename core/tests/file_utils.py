import os
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO

def create_inmemory_file(file_name='tmp.txt', content=b'', content_type=None):
    stream = BytesIO()
    stream.write(content)
    file = InMemoryUploadedFile(stream, None, file_name, content_type, stream.tell(), None)
    file.seek(0)
    return file


def create_inmemory_image(file_name='tmp.png', format=None, width=200,
    height=200, content_type=None):
    from PIL import Image
    if not format:
        _, extension = os.path.splitext(file_name)
        format = extension[1:].upper()
    if not content_type:
        content_type = 'image/{0}'.format(format)
    stream = BytesIO()
    size = (width, height)
    color = (255, 0, 0, 0)
    image = Image.new('RGBA', size, color)
    image.save(stream, format=format)
    image_file = InMemoryUploadedFile(stream, None, file_name, content_type, stream.tell(), None)
    image_file.seek(0)
    return image_file
