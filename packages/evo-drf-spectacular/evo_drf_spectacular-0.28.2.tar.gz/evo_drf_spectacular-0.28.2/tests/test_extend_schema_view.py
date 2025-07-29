import pytest
from django.db import models
from rest_framework import mixins, routers, serializers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.test import APIClient

from drf_spectacular.generators import SchemaGenerator
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, extend_schema_view
from tests import assert_schema


class ESVModel(models.Model):
    pass


class ESVSerializer(serializers.ModelSerializer):
    class Meta:
        model = ESVModel
        fields = '__all__'


class DualMethodActionParamsSerializer(serializers.Serializer):
    message = serializers.CharField()


@extend_schema(tags=['global-tag'])
@extend_schema_view(
    list=extend_schema(description='view list description'),
    retrieve=extend_schema(description='view retrieve description'),
    extended_action=extend_schema(description='view extended action description'),
    raw_action=extend_schema(description='view raw action description'),
    dual_method_action=[
        extend_schema(parameters=[DualMethodActionParamsSerializer], methods=['GET']),
        extend_schema(request=DualMethodActionParamsSerializer, methods=['POST']),
    ]
)
class XViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = ESVModel.objects.all()
    serializer_class = ESVSerializer

    @extend_schema(tags=['custom-retrieve-tag'])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(responses=OpenApiTypes.DATE)
    @action(detail=False)
    def extended_action(self, request):
        return Response('2020-10-31')

    @action(detail=False, methods=['GET'])
    def raw_action(self, request):
        return Response('2019-03-01')

    @extend_schema(description='view dual method action description')
    @action(detail=False, methods=['GET', 'POST'])
    def dual_method_action(self, request):
        if request.method == 'POST':
            data = request.data
        else:
            data = request.query_params
        return Response(data['message'])


# view to make sure there is no cross-talk
class YViewSet(viewsets.ModelViewSet):
    serializer_class = ESVSerializer
    queryset = ESVModel.objects.all()


# view to make sure that schema applied to a subclass does not affect its parent.
@extend_schema_view(
    list=extend_schema(exclude=True),
    retrieve=extend_schema(description='overridden description for child only'),
    extended_action=extend_schema(responses={200: {'type': 'string', 'pattern': r'^[0-9]{4}(?:-[0-9]{2}){2}$'}}),
    raw_action=extend_schema(summary="view raw action summary"),
)
class ZViewSet(XViewSet):
    @extend_schema(tags=['child-tag'])
    @action(detail=False, methods=['GET'])
    def raw_action(self, request):
        return Response('2019-03-01')  # pragma: no cover


router = routers.SimpleRouter()
router.register('x', XViewSet)
router.register('y', YViewSet, basename='alt1')
router.register('z', ZViewSet, basename='alt2')
urlpatterns = router.urls


@pytest.mark.urls(__name__)
def test_extend_schema_view(no_warnings):
    assert_schema(
        SchemaGenerator().get_schema(request=None, public=True),
        'tests/test_extend_schema_view.yml'
    )


@pytest.mark.urls(__name__)
@pytest.mark.django_db
def test_extend_schema_view_call_transparency(no_warnings):
    ESVModel.objects.create()

    response = APIClient().get('/x/')
    assert response.status_code == 200
    assert response.content == b'[{"id":1}]'
    response = APIClient().get('/x/1/')
    assert response.status_code == 200
    assert response.content == b'{"id":1}'
    response = APIClient().get('/x/extended_action/')
    assert response.status_code == 200
    assert response.content == b'"2020-10-31"'
    response = APIClient().get('/x/raw_action/')
    assert response.status_code == 200
    assert response.content == b'"2019-03-01"'
    response = APIClient().get('/x/dual_method_action/', {'message': 'foo bar'})
    assert response.status_code == 200
    assert response.content == b'"foo bar"'
    response = APIClient().post('/x/dual_method_action/', {'message': 'foo bar'})
    assert response.status_code == 200
    assert response.content == b'"foo bar"'
