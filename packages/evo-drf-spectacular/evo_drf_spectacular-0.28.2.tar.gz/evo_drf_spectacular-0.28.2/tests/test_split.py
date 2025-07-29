from unittest import mock

from django.db import models
from rest_framework import mixins, parsers, serializers, viewsets

from tests import assert_schema, generate_schema


class PNM1(models.Model):
    field = models.IntegerField()


class PNM2(models.Model):
    field_relation = models.ForeignKey(PNM1, on_delete=models.CASCADE)
    field_non_blank = models.CharField(max_length=5)


class XSerializer(serializers.ModelSerializer):
    class Meta:
        model = PNM1
        fields = '__all__'


class YSerializer(serializers.ModelSerializer):
    field_relation = XSerializer()
    field_relation_partial = XSerializer(source='field_relation', partial=True)

    class Meta:
        model = PNM2
        fields = '__all__'


class XViewset(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    parser_classes = [parsers.JSONParser]
    serializer_class = YSerializer
    queryset = PNM2.objects.all()


@mock.patch('drf_spectacular.settings.spectacular_settings.COMPONENT_SPLIT_REQUEST', False)
def test_nested_partial_on_split_request_false(no_warnings, django_transforms):
    # without split request, PatchedY and Y have the same properties (minus required).
    # PATCH only modifies outermost serializer, nested serializers must stay unaffected.
    assert_schema(
        generate_schema('x', XViewset),
        'tests/test_split_request_false.yml',
        transforms=django_transforms
    )


@mock.patch('drf_spectacular.settings.spectacular_settings.COMPONENT_SPLIT_REQUEST', True)
def test_nested_partial_on_split_request_true(no_warnings, django_transforms):
    # with split request, behaves like above, however response schemas are always unpatched.
    # nested request serializers are only affected by their manual partial flag and not due to PATCH.
    assert_schema(
        generate_schema('x', XViewset),
        'tests/test_split_request_true.yml',
        transforms=django_transforms,
    )
