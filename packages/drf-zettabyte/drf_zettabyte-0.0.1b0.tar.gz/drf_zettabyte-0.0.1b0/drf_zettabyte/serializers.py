from rest_framework import serializers

import serpy


class BaseModelSerializer(serializers.ModelSerializer):
    def __init__(self, instance=None, data=serializers.empty, **kwargs):
        super().__init__(instance, data, **kwargs)

        excluded_fields = self.Meta.model.get_excluded_fields()
        for field_name in excluded_fields:
            if field_name in self.fields:
                self.fields.pop(field_name)


class BaseModelSerpySerializer(serpy.Serializer):
    id = serpy.IntField()

    def to_value(self, instance):
        fields = self._compiled_fields
        if self.many:
            serialize = self._serialize
            return [serialize(o, fields) for o in instance]

        if instance is None:
            return None

        return self._serialize(instance, fields)
