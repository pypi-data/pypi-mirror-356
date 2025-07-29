from rest_framework import exceptions
from rest_framework.permissions import DjangoModelPermissions


class CustomDjangoModelPermissions(DjangoModelPermissions):
    perms_map = {
        "GET": ["%(app_label)s.view_%(model_name)s"],
        "OPTIONS": ["%(app_label)s.view_%(model_name)s"],
        "HEAD": ["%(app_label)s.view_%(model_name)s"],
        "POST": ["%(app_label)s.add_%(model_name)s"],
        "PUT": ["%(app_label)s.change_%(model_name)s"],
        "PATCH": ["%(app_label)s.change_%(model_name)s"],
        "DELETE": ["%(app_label)s.delete_%(model_name)s"],
    }

    def is_action(self, request):
        path = request.path_info.strip("/")

        parts = path.split("/")

        if len(parts) >= 4 and parts[0] == "v1":
            if (len(parts) == 5) or (len(parts) == 4):
                return True

        return False

    def get_action_endpoint(self, request):
        path = request.path_info.strip("/")
        parts = path.split("/")

        if len(parts) >= 4 and parts[0] == "v1":
            if len(parts) == 5:
                return parts[4]

            if len(parts) == 4:
                return parts[3]

        raise ValueError("O endpoint da request atual não possui uma action")

    def get_required_permissions(self, request, model_cls):
        kwargs = {
            "app_label": model_cls._meta.app_label,
            "model_name": model_cls._meta.model_name,
        }

        if request.method not in self.perms_map:
            raise exceptions.MethodNotAllowed(request.method)

        if self.is_action(request):
            action = self.get_action_endpoint(request)
            return [perm % kwargs for perm in self.perms_map[action]]

        return [perm % kwargs for perm in self.perms_map[request.method]]

    def has_permission(self, request, view):
        if not request.user or (
            not request.user.is_authenticated and self.authenticated_users_only
        ):
            return False

        if getattr(view, "_ignore_model_permissions", False):
            return True

        queryset = self._queryset(view)
        perms = self.get_required_permissions(request, queryset.model)

        return request.user.has_perms(perms)
