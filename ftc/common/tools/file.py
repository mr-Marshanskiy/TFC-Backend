from io import BytesIO

import requests
from PIL import Image


def download_file(url, file_path, request=requests):
    get_response = request.get(url, stream=True)
    with open(file_path, 'wb') as f:
        for chunk in get_response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)


def crop_image(image, image_data):
    img_io = BytesIO()
    image = Image.open(image.file)
    ratio = image_data.get('ratio', 1)
    format = image.format

    rotate = image_data.get('rotate', 0)
    if rotate != 0:
        image = image.rotate(-rotate if rotate > 0 else abs(rotate), expand=True)

    if image_data.get('scaleX') and image_data.get('scaleX') == -1:
        image = image.transpose(Image.FLIP_LEFT_RIGHT)
    if image_data.get('scaleY') and image_data.get('scaleY') == -1:
        image = image.transpose(Image.FLIP_TOP_BOTTOM)

    if ratio > 1:
        new_width, new_height = image.size
        resized_image = image.resize((int(new_width * ratio), int(new_height * ratio)), Image.ANTIALIAS)
        resized_image.format = format
        image = resized_image

    cropped_image = image.crop((
        image_data.get('x', 0) * ratio,
        image_data.get('y', 0) * ratio,
        image_data.get('width') * ratio + image_data.get('x', 0) * ratio,
        image_data.get('height') * ratio + image_data.get('y', 0) * ratio
    ))

    cropped_image.save(img_io, format)

    return img_io