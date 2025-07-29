import copy
import json
import uuid

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.forms.models import model_to_dict
from django.utils.translation import gettext_lazy as _

from auditlog.models import AuditlogHistoryField
from django_islands.fields import TenantForeignKey
from django_islands.models import TenantModel, TenantManager
from django_islands.utils import get_current_tenant
from threadlocals.threadlocals import get_current_user

from drf_zettabyte.extensions.back_blaze.bucket import BackBlazeB2Handler


class CustomTenantManager(TenantManager):
    def serialize(self, *fields):
        relational_fields = self.model.get_relational_fields_names()

        fk_fields = []
        for field in fields:
            base_field = field.split("__")[0]
            if base_field in relational_fields and base_field not in fk_fields:
                fk_fields.append(base_field)

        queryset = self.get_queryset()

        if fk_fields:
            queryset = queryset.select_related(*fk_fields)

        queryset = queryset.only(*fields).values(*fields)

        return list(queryset)


class Base(TenantModel):
    bucket_entity = None
    default_bucket_path = None

    default_exclude_fields = [
        "ativo",
        "codigo",
        "data_criacao",
        "hora_criacao",
        "data_ultima_alteracao",
        "hora_ultima_alteracao",
        "filial",
        "owner",
        "assinatura",
    ]

    exclude_fields = []

    ativo = models.BooleanField(_("ativo"), default=True)
    codigo = models.PositiveBigIntegerField(_("código"), editable=False, default=1)
    data_criacao = models.DateField(_("data de criação"), auto_now_add=True)
    hora_criacao = models.TimeField(_("hora de criação"), auto_now_add=True)
    data_ultima_alteracao = models.DateField(_("data da última alteração"), auto_now=True)
    hora_ultima_alteracao = models.TimeField(_("hora da última alteração"), auto_now=True)
    owner = TenantForeignKey(
        verbose_name=_("owner"),
        to=settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
    )

    history = AuditlogHistoryField()

    all_objects = models.Manager()

    def as_dict(self):
        data = model_to_dict(self)
        excluded_fields = self.get_excluded_fields()
        for field in excluded_fields:
            if field in data:
                del data[field]
        return data

    def as_json(self):
        data = self.as_dict()
        return json.dumps(data, default=str)

    def clonar(self, **fields):
        clone = copy.copy(self)
        clone.pk = None
        for chave, valor in fields.items():
            setattr(clone, chave, valor)
        clone.save()
        return clone

    def upload_arquivo(self, arquivo):
        if self.default_bucket_path is None:
            raise ValueError(
                f"O atributo 'default_bucket_path' não foi preenchido na classe {self.__class__.__name__}"
            )

        assinatura = get_current_tenant()
        extencao = arquivo.name.split(".")[-1]
        uuid_aleatorio = uuid.uuid4()
        novo_nome_arquivo = f"{uuid_aleatorio}.{extencao}"
        conteudo_arquivo = arquivo.read()

        path = self.default_bucket_path % (assinatura.pk, self.pk, novo_nome_arquivo)

        handler = BackBlazeB2Handler()
        file_version = handler.upload(conteudo_arquivo, path)

        content_type = ContentType.objects.get_for_model(self.__class__)
        bucket_url = f"{handler.BASE_URL}{path}"
        upload = Upload.objects.create(
            ld_content_type=content_type,
            ld_registro_id=self.pk,
            ld_registro=self,
            ld_back_blaze_id=file_version.id_,
            ld_back_blaze_path=bucket_url,
            ld_back_blaze_url=path,
        )

        return upload

    def delete_upload(self, upload):
        handler = BackBlazeB2Handler()
        response = handler.destroy(upload.ld_back_blaze_id, upload.ld_back_blaze_path)
        return response

    def save(self, *args, **kwargs):
        if not hasattr(self, "owner"):
            if self.system_model:
                user_cls = get_user_model()
                self.owner = user_cls.get_instacia_bot_wcommanda()
            else:
                self.owner = get_current_user()

        if self.pk is None:
            max_code = (
                self.__class__.objects.all().aggregate(max=models.Max("codigo"))["max"]
                or 0
            )
            self.codigo = max_code + 1

        return super().save(*args, **kwargs)

    @classmethod
    def get_column_names(cls):
        return [field.name for field in cls._meta.get_fields() if field.concrete]

    @classmethod
    def get_serializable_column_names(cls):
        fields = cls.get_column_names()
        excluded_fields = cls.get_excluded_fields()
        return [field for field in fields if field not in excluded_fields]

    @classmethod
    def get_excluded_fields(cls):
        return cls.default_exclude_fields + cls.exclude_fields

    @classmethod
    def get_relational_fields_names(cls):
        return [
            field.name
            for field in cls._meta.get_fields()
            if field.concrete and field.is_relation
        ]

    class Meta:
        abstract = True


class Upload(Base):
    ld_content_type = models.ForeignKey(
        verbose_name=_("content type"),
        to="contenttypes.ContentType",
        on_delete=models.PROTECT,
    )
    ld_registro_id = models.PositiveBigIntegerField(_("id do registro"))
    ld_registro = GenericForeignKey("ld_content_type", "ld_registro_id")
    ld_back_blaze_id = models.CharField(_("id do upload no back blaze"), max_length=256)
    ld_back_blaze_path = models.CharField(_("path do bucket back blaze"), max_length=256)
    ld_back_blaze_url = models.CharField(_("url amigável back blaze"), max_length=256)

    class Meta:
        db_table = "drf_zettabyte_upload"
        ordering = ["-id"]
        verbose_name = _("Upload")
        verbose_name_plural = _("Uploads")


class EstadosChoices(models.IntegerChoices):
    EM_BRANCO = 0, "Em branco"
    RONDONIA = 1, "Rondônia"
    ACRE = 2, "Acre"
    AMAZONAS = 3, "Amazonas"
    RORAIMA = 4, "Roraima"
    PARA = 5, "Pará"
    AMAPA = 6, "Amapá"
    TOCANTINS = 7, "Tocantins"
    MARANHAO = 8, "Maranhão"
    PIAUI = 9, "Piauí"
    CEARA = 10, "Ceará"
    RIO_GRANDE_DO_NORTE = 11, "Rio Grande do Norte"
    PARAIBA = 12, "Paraíba"
    PERNAMBUCO = 13, "Pernambuco"
    ALAGOAS = 14, "Alagoas"
    SERGIPE = 15, "Sergipe"
    BAHIA = 16, "Bahia"
    MINAS_GERAIS = 17, "Minas Gerais"
    ESPIRITO_SANTO = 18, "Espírito Santo"
    RIO_DE_JANEIRO = 19, "Rio de Janeiro"
    SAO_PAULO = 20, "São Paulo"
    PARANA = 21, "Paraná"
    SANTA_CATARINA = 22, "Santa Catarina"
    RIO_GRANDE_DO_SUL = 23, "Rio Grande do Sul"
    MATO_GROSSO_DO_SUL = 24, "Mato Grosso do Sul"
    MATO_GROSSO = 25, "Mato Grosso"
    GOIAS = 26, "Goiás"
    DISTRITO_FEDERAL = 27, "Distrito Federal"
    EXTERIOR = 28, "Exterior"
