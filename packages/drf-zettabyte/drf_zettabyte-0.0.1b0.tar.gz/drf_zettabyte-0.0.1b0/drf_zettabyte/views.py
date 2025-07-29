import warnings

from django.db.models import ProtectedError

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from django_islands.utils import get_current_tenant


class BaseModelViewSet(ModelViewSet):
    # drf attrs
    serializer_classes = {}
    serializer_class = None
    search_fields = []
    ordering_fields = []

    # custom attrs
    use_list_serializer = False
    use_grid_serializer = True

    def check_permissions(self, request):
        base_permissions = {
            "grid": ["%(app_label)s.view_%(model_name)s"],
            "form": ["%(app_label)s.view_%(model_name)s"],
            "ativar": ["%(app_label)s.ativar_inativar_%(model_name)s"],
            "inativar": ["%(app_label)s.ativar_inativar_%(model_name)s"],
        }

        for permission in self.get_permissions():
            if issubclass(permission.__class__, DjangoModelPermissions):
                permission.perms_map = {
                    **permission.perms_map,
                    **base_permissions,
                    **self.aditional_permissions,
                }

            if not permission.has_permission(request, self):
                self.permission_denied(
                    request,
                    message=getattr(permission, "message", None),
                    code=getattr(permission, "code", None),
                )

    def get_object(self, as_instance=True):
        queryset = self.filter_queryset(self.get_queryset())

        relation_fields = queryset.model.get_relational_fields_names()
        queryset = self.set_queryset_aditional_data_default(
            queryset.select_related(*relation_fields)
        )

        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            f"Expected view {self.__class__.__name__} to be called with a URL keyword argument "
            f'named "{lookup_url_kwarg}". Fix your URL conf, or set the `.lookup_field` '
            "attribute on the view correctly."
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}

        if as_instance:
            instance = get_object_or_404(queryset, **filter_kwargs)
        else:
            fields = queryset.model.get_serializable_column_names()
            instance = get_object_or_404(
                queryset.only(*fields).values(*fields), **filter_kwargs
            )

        self.check_object_permissions(self.request, instance)

        self.instance = instance

        return instance

    def set_queryset_aditional_data_default(self, queryset):
        return queryset

    def get_queryset(self):
        queryset = self.set_queryset_aditional_data_default(super().get_queryset())

        method = getattr(self, f"set_queryset_aditional_data_{self.action}", None)
        if method:
            queryset = method(queryset)

        return queryset.filter(assinatura=get_current_tenant())

    def get_serializer_class(self):
        assert self.serializer_classes != {} or self.serializer_class is not None, (
            f"'{self.__class__.__name__}' deve implementar o 'serializer_class' ou  'serializer_classes'."
        )

        if self.serializer_class:
            if self.serializer_class is not None and self.serializer_classes != {}:
                warnings.warn(
                    f"'{self.__class__.__name__}' possui o 'serializer_class' e 'serializer_classes'. O 'serializer_classes' será ignorado.",
                    stacklevel=1,
                )

            return self.serializer_class

        if self.action not in self.serializer_classes:
            raise AssertionError(
                f"'{self.__class__.__name__}' não possui um serializer para a ação '{self.action}'."
            )

        return self.serializer_classes[self.action]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        aditional_context = self.get_aditional_serializer_context()
        return {
            "action": self.action,
            "token": self.request.headers.get("Authorization"),
            **context,
            **aditional_context,
        }

    def get_aditional_serializer_context(self):
        return {}

    def perform_create(self, serializer, **overwrite):
        return serializer.save(**overwrite)

    def perform_update(self, serializer, **overwrite):
        return serializer.save(**overwrite)

    def alter_unique_fields(self, instance):
        pass

    def generic_action(self, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_status = kwargs.get("status", status.HTTP_200_OK)
        response_data = kwargs.get("data", None)
        return Response(response_data, status=response_status)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if self.use_list_serializer:
            page = self.paginate_queryset(queryset)
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        fields = queryset.model.get_serializable_column_names()
        page = self.paginate_queryset(queryset.values(*fields))
        return self.get_paginated_response(page)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object(as_instance=False)
        return Response(instance)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ProtectedError as e:
            return Response(
                {
                    "message": "this record has already been used by the database",
                    "relations": [r.as_dict() for r in e.protected_objects],
                },
                status=status.HTTP_409_CONFLICT,
            )

    @action(methods=["get"], detail=False)
    def grid(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(methods=["get"], detail=True)
    def form(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(methods=["post"], detail=True)
    def clonar(self, request, pk):
        instance = self.get_object()
        clone = instance.clonar()
        self.alter_unique_fields(clone)
        clone.save()
        serializer = self.get_serializer(clone)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=["post"], detail=True)
    def ativar(self, request, pk):
        instance = self.get_object()
        instance.ativo = True
        instance.save(update_fields=["ativo"])
        return Response()

    @action(methods=["post"], detail=True)
    def inativar(self, request, pk):
        instance = self.get_object()
        instance.ativo = False
        instance.save()
        return Response()
