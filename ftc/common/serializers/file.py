from django.core.files.base import ContentFile

from common.tools.file import crop_image

from io import BytesIO

from PIL import Image
from rest_framework import serializers

from common.models.file import File


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        exclude = ('created_at', 'updated_at')

    def create(self, validated_data):
        try:
            if 'image' in validated_data['file'].content_type:
                image = Image.open(validated_data['file'])
                format = image.format

                output = BytesIO()
                image.save(output, format=format)
                output.seek(0)

                validated_data['file'].file = output
        except Exception:
            pass

        return super(FileSerializer, self).create(validated_data)


class CropSerializer(serializers.ModelSerializer):
    class Meta:
        image_field = 'image'
        crop_field = 'crop'

    crop_url = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
    coords = serializers.JSONField(default=False, write_only=True)
    cropped_data = serializers.SerializerMethodField()

    def get_crop_url(self, obj):
        crop = getattr(obj, self.Meta.crop_field)
        return crop.file.url if crop else None

    def get_cropped_data(self, obj):
        request = self.context.get('request')

        crop_obj = getattr(obj, self.Meta.crop_field)
        photo_obj = getattr(obj, self.Meta.image_field)

        crop = crop_obj if crop_obj and crop_obj.file else None
        photo = photo_obj if photo_obj and photo_obj.file else None

        return {
            'photo': photo.pk if photo else None,
            'photo_url': request.build_absolute_uri(photo.file.url) if photo else None,
            'crop_url': request.build_absolute_uri(crop.file.url) if crop else None
        }

    def get_image_url(self, obj):
        img = getattr(obj, self.Meta.image_field)
        return img.file.url if img else None

    def create(self, validated_data):
        coords = validated_data.get('coords', None)
        image = validated_data.get(self.Meta.image_field, None)

        if coords and image:
            img_io = crop_image(image, coords)
            photo_crop = ContentFile(img_io.getvalue(), 'photo_crop.jpg')
            crop_photo_obj = File(file=photo_crop, file_name='photo_crop.jpg')
            crop_photo_obj.save()
            validated_data['crop'] = crop_photo_obj

        validated_data.pop('coords', None)

        return super(CropSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        image_field = self.Meta.image_field
        crop_field = self.Meta.crop_field

        coords = validated_data.get('coords', None)

        instance_image = None
        instance_crop = None

        update_fields = []

        image = validated_data.get(image_field, getattr(instance, image_field))

        if image and image != getattr(instance, image_field):
            instance_image = getattr(instance, image_field)
            validated_data[image_field] = image
            update_fields.append(image_field)

        if coords:
            instance_crop = getattr(instance, crop_field)
            img_io = crop_image(image, coords)
            photo_crop = ContentFile(img_io.getvalue(), 'photo_crop.jpg')
            crop_photo_obj = File(file=photo_crop, file_name='photo_crop.jpg')
            crop_photo_obj.save()
            validated_data[crop_field] = crop_photo_obj
            update_fields.append(crop_field)

        validated_data.pop('coords', None)

        if instance_image:
            instance_image.file.delete()
            instance_image.delete()

        if instance_crop:
            instance_crop.file.delete()
            instance_crop.delete()

        return super(CropSerializer, self).update(instance, validated_data)
