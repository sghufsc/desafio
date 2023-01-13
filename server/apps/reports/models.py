from marshmallow import fields
from server.models import BaseModel, LocalTime
from server.apps.hardware.validators import validate_group


class Report(BaseModel):
    """
    Relatório

    Instância de relatório salva no Banco de Dados

    """
    group_id = fields.String(required=True, validate=validate_group)
    start_at = fields.Date(required=True)
    end_at = fields.Date(required=True)
    create_at = LocalTime()