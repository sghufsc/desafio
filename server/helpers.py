from flask import Blueprint
from server.models import BaseModel


def register_route(url: str, collection:str, api: BaseModel, bp: Blueprint):
    """
    Registro de rotas da aplicação

    """

    METHODS_DICT = {
        "list": {"verb": "GET", "many": True},
        "retrieve": {"verb": "GET", "many": False},
        "create": {"verb": "POST", "many": False},
        "update": {"verb": "PUT", "many": False},
        "delete": {"verb": "DELETE", "many": False},
        "partial_update": {"verb": "PATCH", "many": False},
    }
    methods = api.methods if "methods" in api.__dict__ else api.base_methods

    for method in methods:
        model = api.model
        instance = api(collection, model)
        method_info = METHODS_DICT.get(method)
        method_func = getattr(instance, method)
        
        url_suffix = '/' if method_info.get('many') else '/<id>'
        bp.add_url_rule(f"{url}{url_suffix}",
                        f"{url}{url_suffix}",
                        method_func,
                        methods=[method_info['verb']])

    return bp
