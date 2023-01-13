from marshmallow import ValidationError
from server.driver import db

def validate_group(group_id: str):
    """
    Verificação se grupo informado no model realmente existe
       
    Args:
        group_id (str): Id do grupo
        
    """

    doc = db().groups.find_one({"_id": group_id})

    if not doc:
        # Grupo não existe
        raise ValidationError(
            f"O grupo '{group_id}' informado não existe no sistema.")