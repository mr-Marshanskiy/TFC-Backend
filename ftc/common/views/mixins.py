from rest_framework.generics import get_object_or_404


class GetObjectFromURL(object):
    """
        Support class for Generics views
    """

    def _get_obj_or_none(self, lookup_field, model):
        obj_id = self.request.parser_context['kwargs'].get(lookup_field)
        obj = model.objects.filter(id=obj_id).first()
        return obj

    def _get_obj(self, lookup_field, model):
        obj_id = self.request.parser_context['kwargs'].get(lookup_field)
        obj = get_object_or_404(model, id=obj_id)
        return obj

    def _get_obj_serializer(self, lookup_field, model):
        obj_id = self.context.get('view').kwargs.get(lookup_field)
        obj = get_object_or_404(model, id=obj_id)
        return obj
