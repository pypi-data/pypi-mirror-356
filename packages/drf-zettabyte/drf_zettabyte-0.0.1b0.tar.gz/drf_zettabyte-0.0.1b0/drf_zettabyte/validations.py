from django.apps import apps
from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _

from django_islands.utils import get_current_tenant


@deconstructible
class UniqueValueValidator(BaseValidator):
    message = "Esse valor já foi utilizado"
    code = "unique_value"

    def __init__(self, model, field_name, message=None, **lookups):
        super().__init__(limit_value=None, message=message)
        self.model_ref = model
        self.field_name = field_name
        self.lookups = lookups

    def __call__(self, value):
        if isinstance(self.model_ref, str):
            app_label, model_name = self.model_ref.split(".")
            Model = apps.get_model(app_label, model_name)
        else:
            Model = self.model_ref

        tenante = get_current_tenant()
        lookup = {
            "ambiente": tenante,
            self.field_name: value,
            **self.lookups,
        }
        if Model.objects.filter(**lookup).exists():
            params = {"value": value}
            raise ValidationError(self.message, code=self.code, params=params)
